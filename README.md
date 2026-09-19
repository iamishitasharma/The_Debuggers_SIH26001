# SIH26001 — AI-Based Landslide Risk Monitoring System (NER)

> **Smart India Hackathon 2026 | Problem Statement SIH26001**
>
> ⚠️ **PROTOTYPE DISCLAIMER:** This is a student prototype built for SIH26001.
> It uses historical and simulated data. It is NOT an official disaster-warning system.
> Do not use for real emergency decisions.

---

## Problem Statement

Design and implement an AI-based early warning and landslide risk monitoring system
for the North Eastern Region (NER) of India. The system should process environmental
data such as rainfall, soil moisture, and terrain slope to predict landslide risk levels
and issue early warnings for high-risk conditions.

## Project Objective

Build a software-only prototype that demonstrates the complete pipeline from:

```
Environmental Data → ML Risk Prediction → GIS Map → Dashboard → Early Warning
```

Target region: Assam, Meghalaya, Nagaland, Manipur, Mizoram, Tripura, Arunachal Pradesh, Sikkim.

---

## Features

| Feature | Status |
|---|---|
| ML risk classification (Low / Moderate / High / Very High) | ✅ |
| Interactive GIS map (Folium + Leaflet.js) | ✅ |
| Streamlit monitoring dashboard | ✅ |
| Flask REST API with 7 endpoints | ✅ |
| Manual prediction form | ✅ |
| CSV batch upload prediction | ✅ |
| Visual alert for High / Very High risk | ✅ |
| Historical incident visualization | ✅ |
| Feature importance chart | ✅ |
| Prediction history log (SQLite) | ✅ |
| Data source labelling (Real / Historical / Simulated) | ✅ |
| Prototype disclaimer on every output | ✅ |
| pytest test suite | ✅ |
| Optional email alert | ✅ (configuration-based) |

---

## Architecture

```
┌─────────────────── STREAMLIT DASHBOARD (dashboard/app.py) ──────────┐
│  Manual Form │  Folium Map  │  Charts  │  History  │  About Model   │
└───────────────────────┬─────────────────────────────────────────────┘
                        │ HTTP (localhost:5000)
┌───────────────────────▼───────────────────────────────────────────────┐
│                 FLASK API  (api/app.py)                               │
│  POST /api/predict          GET /api/summary                         │
│  POST /api/predict/batch    GET /api/incidents                       │
│  GET  /api/history          GET /api/feature-importance              │
│  GET  /api/health           GET /api/model-info                      │
└───────────┬───────────────────────────────────────┬───────────────────┘
            │                                       │
┌───────────▼──────────┐                ┌───────────▼────────┐
│  ml/predictor.py     │                │  api/database.py   │
│  RandomForestClassif.│                │  SQLite            │
│  landslide_model.pkl │                │  predictions.db    │
└──────────────────────┘                └────────────────────┘

┌─────────────── OFFLINE TRAINING (run once) ───────────────────┐
│  python data/generate_sample_data.py                          │
│  python ml/train_model.py   →  ml/models/landslide_model.pkl │
└───────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| ML Model | scikit-learn RandomForestClassifier |
| Data Processing | pandas, numpy |
| Class Balancing | imbalanced-learn (SMOTE) |
| Model Persistence | joblib |
| Backend API | Python Flask 3 |
| Dashboard UI | Streamlit |
| GIS Map | Folium + streamlit-folium |
| Database | SQLite (built-in Python sqlite3) |
| Email Alerts | smtplib (built-in, optional) |
| Testing | pytest |

---

## Dataset Structure

### `data/training_data.csv`

| Column | Type | Description |
|---|---|---|
| location_name | string | District name |
| latitude / longitude | float | WGS84 coordinates |
| rainfall_mm | float | Daily rainfall (mm) |
| soil_moisture_pct | float | Soil moisture (0–100%) |
| slope_angle_deg | float | Terrain slope (0–80°) |
| ndvi | float | Vegetation index (−1 to 1) |
| lithology_code | int | Rock/soil type (1–5) |
| risk_level | int | Target: 0=Low, 1=Moderate, 2=High, 3=Very High |
| data_source | string | Always "Simulated" for generated data |

### `data/historical_incidents.csv`

Illustrative records of reported NER landslide events, labelled `Reported/Simulated`.

---

## ML Approach

**Algorithm:** Random Forest Classifier

**Why Random Forest?**
- Better accuracy than a single Decision Tree
- Provides `feature_importances_` for explainability
- Works well on tabular data without extensive tuning
- `class_weight='balanced'` handles imbalanced risk classes
- No need for complex feature engineering

**Training pipeline:**
1. Load and validate `data/training_data.csv`
2. Stratified 80/20 train/test split
3. `StandardScaler` fitted on training data only (prevents data leakage)
4. SMOTE applied to training set only (balances minority classes)
5. Train `RandomForestClassifier(n_estimators=100, max_depth=12, class_weight='balanced')`
6. Evaluate on held-out test set (accuracy, macro F1, confusion matrix)
7. Save `landslide_model.pkl` and `scaler.pkl`

**Primary evaluation metric:** Macro F1-Score (equal weight to all 4 classes)

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-team/sih26001-landslide.git
cd sih26001-landslide
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate demo data

```bash
python data/generate_sample_data.py
```

This creates:
- `data/training_data.csv` — 1500-row simulated training dataset
- `data/historical_incidents.csv` — 25 illustrative NER incidents
- `data/sample_batch_input.csv` — 10-row demo for batch upload

### 5. Train the model

```bash
python ml/train_model.py
```

This produces:
- `ml/models/landslide_model.pkl`
- `ml/models/scaler.pkl`
- `ml/models/feature_columns.json`
- `ml/artifacts/confusion_matrix.png`
- `ml/artifacts/feature_importance.png`
- `ml/artifacts/classification_report.txt`

### 6. Start the Flask API

```bash
python api/app.py
```

API will be available at `http://127.0.0.1:5000`

### 7. Start the Streamlit dashboard

In a **second terminal** (with `.venv` active):

```bash
streamlit run dashboard/app.py
```

Dashboard opens at `http://localhost:8501`

---

## How to Retrain the Model

If you have new data, replace `data/training_data.csv` with the updated file (keeping the same column structure), then run:

```bash
python ml/train_model.py
```

The new model will overwrite `ml/models/landslide_model.pkl`. Restart the Flask API to load the new model.

---

## API Usage

### Health Check

```bash
curl http://localhost:5000/api/health
```

### Single Prediction

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "location_name": "Gangtok",
    "latitude": 27.33,
    "longitude": 88.62,
    "rainfall_mm": 180.0,
    "soil_moisture_pct": 85.0,
    "slope_angle_deg": 50.0,
    "ndvi": 0.25,
    "lithology_code": 5,
    "data_source": "Demo"
  }'
```

Response:
```json
{
  "risk_level": "Very High",
  "risk_code": 3,
  "confidence": 0.87,
  "color": "#e74c3c",
  "alert": true,
  "disclaimer": "PROTOTYPE ONLY — ...",
  "timestamp": "2025-07-10T14:30:00+00:00"
}
```

### Batch Prediction

```bash
curl -X POST http://localhost:5000/api/predict/batch \
  -F "file=@data/sample_batch_input.csv"
```

### Other Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/history?limit=50` | Recent predictions |
| GET | `/api/summary` | Risk level counts |
| GET | `/api/incidents` | Historical incidents |
| GET | `/api/feature-importance` | Feature importances |
| GET | `/api/model-info` | Model metadata |

---

## Testing

```bash
pytest tests/ -v
```

Tests that require a trained model are automatically skipped if `ml/models/landslide_model.pkl` does not exist.

To run only data/validation tests (no model needed):

```bash
pytest tests/test_data_loader.py tests/test_database.py -v
```

---

## Optional Email Alerts

1. Copy `.env.example` to `.env`
2. Fill in your Gmail credentials (use an App Password, not your real password)
3. Restart the Flask API

Email alerts fire when a prediction returns Very High risk and the API is running.

---

## Demo Instructions for SIH Judges

1. **Start both servers** (Steps 6 and 7 above)
2. Open the dashboard at `http://localhost:8501`
3. Navigate through:
   - **🏠 Overview Dashboard** — shows risk summary and feature importance
   - **🔍 Predict Risk** — enter values for Gangtok (high-rainfall scenario) and observe red alert
   - **🗺️ Risk Map** — observe colour-coded markers; toggle incident layer
   - **📜 Historical Incidents** — filter by state/severity
   - **🤖 About the Model** — show confusion matrix, feature importance, limitations
4. **Demo the API directly** — open a terminal and run the curl command above
5. **Demo batch upload** — upload `data/sample_batch_input.csv` from the Predict Risk page

---

## Limitations

1. Trained on simulated/historical data — operational accuracy on real future events is unknown
2. Not connected to live sensor networks or real-time weather APIs
3. No temporal modelling — multi-day rainfall accumulation is not captured
4. Labels are rule-derived, not field-validated
5. SQLite is not suitable for production-scale concurrent access
6. Email alerts require Gmail App Password configuration
7. Village-level resolution is not supported (district-level only)

---

## Future Improvements

- Integration with IMD real-time rainfall API
- SMAP satellite soil moisture feed
- Time-series LSTM model for temporal patterns
- SMS alerts via MSG91
- Mobile app for field data entry
- PostgreSQL + PostGIS for production database
- Village-level GIS resolution
- Integration with SDMA/NDRF alert systems

---

## Team

| Member | Role | Files Owned |
|---|---|---|
| Member 1 | ML Engineer | `ml/preprocess.py`, `ml/train_model.py`, `ml/evaluate_model.py` |
| Member 2 | Backend/API Developer | `api/app.py`, `api/predictor.py`, `api/database.py`, `api/alerts.py` |
| Member 3 | Dashboard Developer | `dashboard/app.py`, `dashboard/components/`, `dashboard/utils/` |
| Member 4 | GIS/Map Developer | `dashboard/components/map_view.py` |
| Member 5 | Data Research | `data/generate_sample_data.py`, `data/training_data.csv` |
| Member 6 | Testing & Documentation | `tests/`, `README.md`, presentation |

---

## Data Sources

| Dataset | Source | Status |
|---|---|---|
| Training data | Synthetically generated (`data/generate_sample_data.py`) | Simulated |
| Historical incidents | Based on publicly reported NER events (approximated) | Reported/Simulated |
| District coordinates | Approximate centroids from public reference | Reference only |
| Real-time data | NOT integrated | Out of scope for prototype |

**Real datasets that should be used in a production system:**
- GSI Bhukosh Landslide Atlas (bhukosh.gsi.gov.in)
- NASA Global Landslide Catalog (catalog.data.gov)
- IMD Gridded Rainfall Data (imdpune.gov.in)
- SRTM Digital Elevation Model (earthdata.nasa.gov)

---

*SIH26001 Student Prototype — Not for Emergency Use*
