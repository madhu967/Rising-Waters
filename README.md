# Rising Waters — Flood Prediction System

Machine learning-powered flood prediction system trained on historical weather data. Uses Decision Tree, Random Forest, KNN, and XGBoost to classify flood risk from meteorological features.

## Project Structure

```
rising waters/
├── data/                    # Flood dataset (from Kaggle)
├── notebooks/               # Jupyter notebooks (Epics 1–4)
├── app/
│   ├── app.py               # Flask application
│   ├── database.py          # ER diagram database models
│   ├── models/              # Saved .pkl model
│   ├── templates/           # HTML pages
│   └── static/css/          # Stylesheets
├── outputs/                 # Generated plots from notebooks
├── train_model.py           # Train and save best model
├── run.py                   # Start Flask app
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
python train_model.py
python run.py
```

Open http://localhost:5000 in your browser.

## Database Schema (ER Diagram)

| Table | Key Fields |
|-------|-----------|
| **Users** | UserID, Name, Email, Password, Role |
| **ML_Model** | ModelID, ModelName, AlgorithmType, Accuracy, ModelFile |
| **Weather_Data** | DataID, UserID, AnnualRainfall, CloudVisibility, Temperature, Humidity, SeasonalRainfall |
| **Prediction_Result** | PredictionID, DataID, ModelID, FloodResult, FloodProbability, PredictionDate |

## Scenarios

1. **Early Warning** — Meteorologist enters rainfall/cloud data; system predicts flood probability.
2. **Resource Allocation** — Coordinator monitors multiple regions via prediction history.
3. **Model Validation** — Analyst reviews model accuracy (XGBoost: 96.55% on test data).

## Dataset

Source: [Kaggle — Rainfall Dataset](https://www.kaggle.com/arbethi/rainfall-dataset)

Features used: Temperature, Humidity, Cloud Cover, Annual Rainfall, Seasonal Rainfall (Jun-Sep).


