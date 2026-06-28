"""Generate Jupyter notebooks for all project epics."""
import json
import os

NOTEBOOKS_DIR = "notebooks"
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)


def nb(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }


def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.split("\n")}


def code(source):
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": source.split("\n"),
    }


notebooks = {
    "01_epic1_data_collection.ipynb": [
        md("# Epic 1: Data Collection\n\n## Story 1: Download and load the flood prediction dataset"),
        code(
            'import os\nimport pandas as pd\n\nDATA_PATH = os.path.join("..", "data", "flood dataset.xlsx")\ndf = pd.read_excel(DATA_PATH)\nprint(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")\ndf.head()'
        ),
        code("df.info()"),
        code("df.describe()"),
    ],
    "02_epic2_visualization_analysis.ipynb": [
        md("# Epic 2: Visualizing and Analysing the Data"),
        code(
            'import os\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nsns.set_style("whitegrid")\nDATA_PATH = os.path.join("..", "data", "flood dataset.xlsx")\ndf = pd.read_excel(DATA_PATH)'
        ),
        md("## Story 2: Explore dataset structure"),
        code("print(df.columns.tolist())\nprint(df['flood'].value_counts())\ndf.head(10)"),
        md("## Story 3: Univariate analysis"),
        code(
            'numeric_cols = df.select_dtypes(include="number").columns\nfig, axes = plt.subplots(3, 3, figsize=(14, 10))\naxes = axes.ravel()\nfor i, col in enumerate(numeric_cols):\n    if i < len(axes):\n        sns.histplot(df[col], kde=True, ax=axes[i])\n        axes[i].set_title(col)\nplt.tight_layout()\nplt.savefig("../outputs/univariate_analysis.png", dpi=120)\nplt.show()'
        ),
        md("## Story 4: Multivariate analysis"),
        code(
            'plt.figure(figsize=(10, 8))\nsns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")\nplt.title("Feature Correlation Matrix")\nplt.tight_layout()\nplt.savefig("../outputs/correlation_heatmap.png", dpi=120)\nplt.show()'
        ),
        code(
            'sns.pairplot(df[["Temp", "Humidity", "Cloud Cover", "ANNUAL", "Jun-Sep", "flood"]], hue="flood", palette="Set1")\nplt.savefig("../outputs/pairplot.png", dpi=120)\nplt.show()'
        ),
        md("## Story 5: Descriptive statistics"),
        code("df.describe().T"),
        code(
            'flood_stats = df.groupby("flood")[["Temp", "Humidity", "Cloud Cover", "ANNUAL", "Jun-Sep"]].mean()\nprint("Mean values by flood class:")\nflood_stats'
        ),
    ],
    "03_epic3_preprocessing.ipynb": [
        md("# Epic 3: Data Pre-Processing"),
        code(
            'import os\nimport pandas as pd\nimport numpy as np\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\n\nDATA_PATH = os.path.join("..", "data", "flood dataset.xlsx")\ndf = pd.read_excel(DATA_PATH)'
        ),
        md("## Story 1: Handle missing values"),
        code("print('Missing values:')\nprint(df.isnull().sum())\ndf = df.dropna()\nprint(f'Rows after drop: {len(df)}')"),
        md("## Story 2: Detect and treat outliers (IQR method)"),
        code(
            'def cap_outliers(series):\n    q1, q3 = series.quantile(0.25), series.quantile(0.75)\n    iqr = q3 - q1\n    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr\n    return series.clip(lower, upper)\n\nfor col in ["ANNUAL", "Jun-Sep", "avgjune"]:\n    df[col] = cap_outliers(df[col])\nprint("Outliers capped for rainfall features")'
        ),
        md("## Story 3: Categorical encoding"),
        code(
            '# Target variable flood is already numeric (0/1)\n# No categorical features require encoding in this dataset\nprint(df.dtypes)'
        ),
        md("## Story 4: Train-test split"),
        code(
            'FEATURES = ["Temp", "Humidity", "Cloud Cover", "ANNUAL", "Jun-Sep"]\nX = df[FEATURES]\ny = df["flood"]\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42, stratify=y\n)\nprint(f"Train: {X_train.shape}, Test: {X_test.shape}")'
        ),
        md("## Story 5: Feature scaling"),
        code(
            'scaler = StandardScaler()\nX_train_scaled = scaler.fit_transform(X_train)\nX_test_scaled = scaler.transform(X_test)\nprint("Features scaled using StandardScaler")\nprint("Sample scaled row:", X_train_scaled[0])'
        ),
    ],
    "04_epic4_model_building.ipynb": [
        md("# Epic 4: Model Building"),
        code(
            'import os\nimport pickle\nimport pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom xgboost import XGBClassifier\nfrom sklearn.metrics import accuracy_score, classification_report, confusion_matrix\nimport matplotlib.pyplot as plt\n\nDATA_PATH = os.path.join("..", "data", "flood dataset.xlsx")\ndf = pd.read_excel(DATA_PATH)\nFEATURES = ["Temp", "Humidity", "Cloud Cover", "ANNUAL", "Jun-Sep"]\nX = df[FEATURES]\ny = df["flood"]\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\nscaler = StandardScaler()\nX_train_s = scaler.fit_transform(X_train)\nX_test_s = scaler.transform(X_test)'
        ),
        md("## Story 1: Decision Tree"),
        code(
            'dt = DecisionTreeClassifier(random_state=42, max_depth=5)\ndt.fit(X_train_s, y_train)\ndt_acc = accuracy_score(y_test, dt.predict(X_test_s))\nprint(f"Decision Tree Accuracy: {dt_acc:.4f}")\nprint(classification_report(y_test, dt.predict(X_test_s)))'
        ),
        md("## Story 2: Random Forest"),
        code(
            'rf = RandomForestClassifier(n_estimators=100, random_state=42)\nrf.fit(X_train_s, y_train)\nrf_acc = accuracy_score(y_test, rf.predict(X_test_s))\nprint(f"Random Forest Accuracy: {rf_acc:.4f}")'
        ),
        md("## Story 3: KNN"),
        code(
            'knn = KNeighborsClassifier(n_neighbors=5)\nknn.fit(X_train_s, y_train)\nknn_acc = accuracy_score(y_test, knn.predict(X_test_s))\nprint(f"KNN Accuracy: {knn_acc:.4f}")'
        ),
        md("## Story 4: XGBoost"),
        code(
            'xgb = XGBClassifier(random_state=42, eval_metric="logloss", n_estimators=150, max_depth=4, scale_pos_weight=6)\nxgb.fit(X_train_s, y_train)\nxgb_acc = accuracy_score(y_test, xgb.predict(X_test_s))\nprint(f"XGBoost Accuracy: {xgb_acc:.4f}")\nprint(classification_report(y_test, xgb.predict(X_test_s)))'
        ),
        md("## Story 5: Compare all models"),
        code(
            'results = {"Decision Tree": dt_acc, "Random Forest": rf_acc, "KNN": knn_acc, "XGBoost": xgb_acc}\nfor name, acc in sorted(results.items(), key=lambda x: -x[1]):\n    print(f"{name}: {acc*100:.2f}%")\n\nplt.bar(results.keys(), [v*100 for v in results.values()], color=["#0d6efd", "#198754", "#ffc107", "#dc3545"])\nplt.ylabel("Accuracy (%)")\nplt.title("Model Comparison")\nplt.ylim(80, 100)\nplt.savefig("../outputs/model_comparison.png", dpi=120)\nplt.show()'
        ),
        md("## Story 6: Save best model"),
        code(
            'best_name = max(results, key=results.get)\nif results.get("XGBoost", 0) >= results[best_name] - 0.02:\n    best_name = "XGBoost"\nmodels = {"Decision Tree": dt, "Random Forest": rf, "KNN": knn, "XGBoost": xgb}\nbest_model = models[best_name]\nartifact = {"model": best_model, "scaler": scaler, "features": FEATURES, "model_name": best_name, "accuracy": results[best_name], "all_results": results}\nmodel_path = os.path.join("..", "app", "models", "best_model.pkl")\nos.makedirs(os.path.dirname(model_path), exist_ok=True)\nwith open(model_path, "wb") as f:\n    pickle.dump(artifact, f)\nprint(f"Saved {best_name} to {model_path}")'
        ),
    ],
}

os.makedirs("outputs", exist_ok=True)

for filename, cells in notebooks.items():
    path = os.path.join(NOTEBOOKS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb(cells), f, indent=1)
    print(f"Created {path}")

print("Done.")
