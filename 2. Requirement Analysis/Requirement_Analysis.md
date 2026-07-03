# Phase 2: Requirement Analysis

## 1. Introduction
The Requirement Analysis phase defines the functional, non-functional, and data requirements for the Rising Waters Flood Prediction System.

## 2. Functional Requirements
These define what the system *should do*:
*   **Data Input:** Users must be able to input the following features manually through a web form: Annual Rainfall, Seasonal Rainfall, Temperature, Humidity, and Cloud Visibility.
*   **Prediction Generation:** The system must process the input data using the pre-trained Machine Learning model.
*   **Result Display:** The application must display the binary outcome (Flood / No Flood) and the calculated probability percentage.
*   **User Management (Future/Optional):** The system should support basic user roles (Admin vs. Standard User) for tracking who is making predictions.

## 3. Non-Functional Requirements
These define *how the system should perform*:
*   **Accuracy:** The underlying predictive model must maintain an accuracy score of >90% (achieved ~96.55% with XGBoost).
*   **Usability:** The web application must be responsive and accessible on standard desktop and mobile browsers.
*   **Performance:** Predictions should be returned in under 2 seconds.
*   **Deployment:** The application structure must remain compatible with standard deployment platforms (e.g., Heroku, Render) without requiring root-level structural changes.

## 4. Data Requirements
*   **Data Source:** Historical Rainfall Dataset (Kaggle).
*   **Features Required:**
    *   `Temperature` (Float)
    *   `Humidity` (Float)
    *   `Cloud Cover` / `Visibility` (Float)
    *   `Annual Rainfall` (Float)
    *   `Seasonal Rainfall` (Jun-Sep) (Float)
*   **Target Variable:** `Flood` (Binary Classification: 1/0 or Yes/No).

## 5. Software & Hardware Requirements
*   **Programming Language:** Python 3.x
*   **Libraries:** Pandas, NumPy, Scikit-learn, XGBoost, Flask
*   **Frontend:** HTML5, CSS3
*   **Development Environment:** Jupyter Notebooks (for EDA and modeling), VS Code / IDE (for application development).
