"""Database models for the Flood Prediction System."""
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="Analyst")

    weather_data = db.relationship("WeatherData", backref="user", lazy=True)
    ml_models = db.relationship("MLModel", backref="user", lazy=True)

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


class MLModel(db.Model):
    __tablename__ = "ml_model"

    model_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    model_name = db.Column(db.String(120), nullable=False)
    algorithm_type = db.Column(db.String(80), nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    model_file = db.Column(db.String(256), nullable=False)

    predictions = db.relationship("PredictionResult", backref="ml_model", lazy=True)


class WeatherData(db.Model):
    __tablename__ = "weather_data"

    data_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    annual_rainfall = db.Column(db.Float, nullable=False)
    cloud_visibility = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    seasonal_rainfall = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    prediction = db.relationship(
        "PredictionResult", backref="weather_data", uselist=False, lazy=True
    )


class PredictionResult(db.Model):
    __tablename__ = "prediction_result"

    prediction_id = db.Column(db.Integer, primary_key=True)
    data_id = db.Column(
        db.Integer, db.ForeignKey("weather_data.data_id"), nullable=False, unique=True
    )
    model_id = db.Column(db.Integer, db.ForeignKey("ml_model.model_id"), nullable=False)
    flood_result = db.Column(db.String(20), nullable=False)
    flood_probability = db.Column(db.Float, nullable=False)
    prediction_date = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
