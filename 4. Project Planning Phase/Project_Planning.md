# Phase 4: Project Planning

## 1. Project Management Timeline

The development of the **Rising Waters** project was divided into logical milestones or "Epics":

### Epic 1: Data Acquisition & Preprocessing
*   **Goal:** Obtain the Kaggle Rainfall Dataset and clean it.
*   **Tasks:** Handle missing values, normalize scales, and perform Exploratory Data Analysis (EDA).

### Epic 2: Model Training & Evaluation
*   **Goal:** Train multiple algorithms and select the best one.
*   **Tasks:** Train Decision Tree, Random Forest, KNN, and XGBoost. Compare accuracy, precision, and recall.
*   **Outcome:** XGBoost selected as the primary model due to superior accuracy.

### Epic 3: Backend Development (Flask)
*   **Goal:** Create a web API that serves the trained model.
*   **Tasks:** Develop `app.py`, integrate `pickle` to load the `.pkl` file, and create routing for web requests.

### Epic 4: Frontend Development
*   **Goal:** Build the user interface.
*   **Tasks:** Develop `templates/*.html` and `static/css/*.css`. Ensure the form connects securely to the Flask backend.

### Epic 5: Deployment & Documentation
*   **Goal:** Make the application available online and document the process.
*   **Tasks:** Configure `Procfile` and `requirements.txt`. Deploy to the cloud. Organize the GitHub repository structure into distinct phases without breaking deployment.

## 2. Resource Allocation
*   **Data Science:** Jupyter Notebooks, `pandas`, `scikit-learn`
*   **Web Development:** `Flask`, HTML/CSS
*   **Version Control:** Git & GitHub
