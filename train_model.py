"""Train flood prediction models and save the best performer."""
import os
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

DATA_PATH = os.path.join("data", "flood dataset.xlsx")
FEATURES = ["Temp", "Humidity", "Cloud Cover", "ANNUAL", "Jun-Sep"]
MODEL_DIR = os.path.join("app", "models")


def main():
    df = pd.read_excel(DATA_PATH)
    X = df[FEATURES]
    y = df["flood"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=5),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "XGBoost": XGBClassifier(
            random_state=42,
            eval_metric="logloss",
            n_estimators=150,
            max_depth=4,
            learning_rate=0.1,
            scale_pos_weight=6,
        ),
    }

    results = {}
    trained = {}
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        preds = model.predict(X_test_scaled)
        acc = accuracy_score(y_test, preds)
        results[name] = acc
        trained[name] = model
        print(f"\n{name} - Accuracy: {acc:.4f}")
        print(classification_report(y_test, preds, target_names=["No Flood", "Flood"]))
        print("Confusion Matrix:\n", confusion_matrix(y_test, preds))

    best_name = max(results, key=results.get)
    best_model = trained[best_name]
    best_accuracy = results[best_name]
    cv_scores = {}
    X_scaled = scaler.fit_transform(X)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for name, model in trained.items():
        cv_scores[name] = float(cross_val_score(model, X_scaled, y, cv=cv).mean())
    print("\nCross-validation scores:")
    for name, score in cv_scores.items():
        print(f"  {name}: {score:.4f}")
    print(f"\nBest model: {best_name} ({best_accuracy:.4f})")

    os.makedirs(MODEL_DIR, exist_ok=True)
    artifact = {
        "model": best_model,
        "scaler": scaler,
        "features": FEATURES,
        "model_name": best_name,
        "accuracy": best_accuracy,
        "cv_scores": cv_scores,
        "all_results": results,
    }
    with open(os.path.join(MODEL_DIR, "best_model.pkl"), "wb") as f:
        pickle.dump(artifact, f)

    return artifact


if __name__ == "__main__":
    main()
