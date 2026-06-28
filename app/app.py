"""Flask web application for flood prediction."""
import os
import pickle
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.database import MLModel, PredictionResult, User, WeatherData, db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "flood-prediction-dev-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'flood_prediction.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    _load_model_artifact(app)

    with app.app_context():
        db.create_all()
        _seed_default_model()

    register_routes(app)
    return app


def _load_model_artifact(app):
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            app.model_artifact = pickle.load(f)
    else:
        app.model_artifact = None


def _seed_default_model():
    if MLModel.query.first() or not os.path.exists(MODEL_PATH):
        return
    artifact = pickle.load(open(MODEL_PATH, "rb"))
    record = MLModel(
        model_name=artifact.get("model_name", "XGBoost_v1"),
        algorithm_type=artifact.get("model_name", "XGBoost"),
        accuracy=float(artifact.get("accuracy", 0.9655)),
        model_file=MODEL_PATH,
    )
    db.session.add(record)
    db.session.commit()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def predict_flood(app, temperature, humidity, cloud_visibility, annual_rainfall, seasonal_rainfall):
    artifact = app.model_artifact
    if artifact is None:
        raise RuntimeError("Model not loaded. Run train_model.py first.")

    features = artifact["features"]
    row = {
        "Temp": temperature,
        "Humidity": humidity,
        "Cloud Cover": cloud_visibility,
        "ANNUAL": annual_rainfall,
        "Jun-Sep": seasonal_rainfall,
    }
    import pandas as pd

    X = pd.DataFrame([row])[features]
    X_scaled = artifact["scaler"].transform(X)
    model = artifact["model"]
    prediction = int(model.predict(X_scaled)[0])
    probability = float(model.predict_proba(X_scaled)[0][1])
    result_label = "Flood" if prediction == 1 else "No Flood"
    return result_label, probability


def register_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            if not all([name, email, password]):
                flash("All fields are required.", "danger")
                return redirect(url_for("register"))

            if User.query.filter_by(email=email).first():
                flash("Email already registered.", "danger")
                return redirect(url_for("register"))

            user = User(name=name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                session["user_id"] = user.user_id
                session["user_name"] = user.name
                session["user_role"] = user.role
                flash(f"Welcome back, {user.name}!", "success")
                return redirect(url_for("dashboard"))

            flash("Invalid email or password.", "danger")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for("index"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        user = User.query.get(session["user_id"])
        recent = (
            WeatherData.query.filter_by(user_id=user.user_id)
            .order_by(WeatherData.created_at.desc())
            .limit(5)
            .all()
        )
        model_record = MLModel.query.first()
        return render_template(
            "dashboard.html", user=user, recent=recent, model_record=model_record
        )

    @app.route("/predict", methods=["GET", "POST"])
    @login_required
    def predict():
        model_record = MLModel.query.first()
        if request.method == "POST":
            try:
                temperature = float(request.form["temperature"])
                humidity = float(request.form["humidity"])
                cloud_visibility = float(request.form["cloud_visibility"])
                annual_rainfall = float(request.form["annual_rainfall"])
                seasonal_rainfall = float(request.form["seasonal_rainfall"])

                weather = WeatherData(
                    user_id=session["user_id"],
                    temperature=temperature,
                    humidity=humidity,
                    cloud_visibility=cloud_visibility,
                    annual_rainfall=annual_rainfall,
                    seasonal_rainfall=seasonal_rainfall,
                )
                db.session.add(weather)
                db.session.flush()

                flood_result, flood_probability = predict_flood(
                    app,
                    temperature,
                    humidity,
                    cloud_visibility,
                    annual_rainfall,
                    seasonal_rainfall,
                )

                if not model_record:
                    flash("No model registered in database.", "danger")
                    return redirect(url_for("predict"))

                prediction = PredictionResult(
                    data_id=weather.data_id,
                    model_id=model_record.model_id,
                    flood_result=flood_result,
                    flood_probability=flood_probability,
                )
                db.session.add(prediction)
                db.session.commit()

                return render_template(
                    "predict.html",
                    model_record=model_record,
                    result={
                        "flood_result": flood_result,
                        "flood_probability": round(flood_probability * 100, 2),
                        "weather": weather,
                    },
                )
            except (ValueError, KeyError):
                flash("Please enter valid numeric values for all fields.", "danger")
            except RuntimeError as exc:
                flash(str(exc), "danger")

        return render_template("predict.html", model_record=model_record, result=None)

    @app.route("/history")
    @login_required
    def history():
        records = (
            db.session.query(WeatherData, PredictionResult)
            .outerjoin(PredictionResult, WeatherData.data_id == PredictionResult.data_id)
            .filter(WeatherData.user_id == session["user_id"])
            .order_by(WeatherData.created_at.desc())
            .all()
        )
        return render_template("history.html", records=records)

    @app.route("/models")
    @login_required
    def models_page():
        models = MLModel.query.order_by(MLModel.accuracy.desc()).all()
        artifact = app.model_artifact or {}
        return render_template(
            "models.html",
            models=models,
            all_results=artifact.get("all_results", {}),
            cv_scores=artifact.get("cv_scores", {}),
        )


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
