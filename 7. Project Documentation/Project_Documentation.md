# Phase 7: Project Documentation

## 1. System Overview
Rising Waters is an automated flood prediction platform. This documentation serves as a guide for both end-users and future developers.

## 2. End-User Manual
### How to Use the Application
1.  Navigate to the deployed web URL.
2.  On the main dashboard, locate the input form.
3.  Enter the required meteorological data:
    *   **Annual Rainfall:** Total rainfall in mm.
    *   **Cloud Visibility:** Percentage of cloud cover.
    *   **Temperature:** Average temperature in Celsius.
    *   **Humidity:** Relative humidity percentage.
    *   **Seasonal Rainfall:** Monsoonal rainfall in mm.
4.  Click **Predict**.
5.  The system will output a "Flood" or "No Flood" alert, alongside a probability percentage.

## 3. Developer Guide
### Local Environment Setup
To run this project locally, ensure you have Python 3 installed.
```bash
# Install dependencies
pip install -r requirements.txt

# (Optional) Re-train the model if data changes
python train_model.py

# Start the Flask development server
python run.py
```
Access the application at `http://localhost:5000`.

### Modifying the ML Model
To replace the XGBoost model with a different algorithm:
1.  Modify `train_model.py`.
2.  Ensure the new model is saved as a `.pkl` file in `app/models/`.
3.  Update the loading logic in `app.py`.
