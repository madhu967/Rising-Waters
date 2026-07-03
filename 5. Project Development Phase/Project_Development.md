# Phase 5: Project Development

## 1. Overview
The Project Development phase involved the actual coding and implementation of the plans defined in the previous phases.



## 2. Key Components Developed

### Data Engineering (`notebooks/`)
Jupyter notebooks were used extensively to clean the Kaggle dataset. Code was written to map categorical variables (like "Yes"/"No") into numerical binaries (1/0) and to split the data into training and testing sets.

### Model Training (`train_model.py`)
This script automates the training pipeline. It reads the preprocessed data, fits the XGBoost classifier, and serializes (pickles) the trained model into the `app/models/` directory for production use.

### The Application Core (`app/app.py` & `run.py`)
The Flask framework was implemented to serve the application.
*   `run.py` acts as the entry point.
*   `app.py` handles the logic: receiving form data via POST requests, formatting the data into a NumPy array, passing it to the loaded model, and rendering the result template.

### Frontend (`app/templates/` & `app/static/`)
HTML templates were built using Jinja2 syntax to dynamically display the prediction results and probabilities returned by the Flask backend.
