# Phase 6: Project Testing

## 1. Testing Strategy

Ensuring the reliability of the **Rising Waters** prediction system involved multiple layers of testing, from data validation to endpoint verification.

## 2. Model Evaluation (Data Science Testing)
The Machine Learning models were tested using a standard 80/20 train-test split. The evaluation metrics used were Accuracy, Precision, Recall, and the F1-Score.

*   **Decision Tree:** ~85% Accuracy
*   **Random Forest:** ~91% Accuracy
*   **K-Nearest Neighbors (KNN):** ~88% Accuracy
*   **XGBoost:** **96.55% Accuracy** (Selected for Production)

The models were tested against edge cases (e.g., extremely high annual rainfall with low cloud visibility) to ensure the predictions logically aligned with meteorological expectations.

## 3. Application Testing (Software Engineering)
*   **Unit Testing:** Individual functions inside `train_model.py` and data transformation logic within the Flask routes were tested to ensure they processed input arrays correctly.
*   **Integration Testing:** Verifying that the Flask application successfully deserialized the `.pkl` model and that the HTML form data successfully mapped to the model's expected feature array.
*   **UI/UX Testing:** The web interface was tested across different screen sizes to ensure responsive design CSS operated correctly. Form validation was tested to prevent users from submitting text instead of numeric data.
