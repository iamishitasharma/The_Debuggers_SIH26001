"""
config.py — Central configuration for SIH26001 Landslide Risk System.

All constants, file paths, thresholds, and risk labels live here.
Import this module in any other module that needs these values.
"""

import os
from pathlib import Path

# ── Project root ──────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent

# ── File paths ────────────────────────────────────────────────────────────────
DATA_DIR          = ROOT_DIR / "data"
RAW_DATA_DIR      = DATA_DIR / "raw"
MODEL_DIR         = ROOT_DIR / "ml" / "models"
ARTIFACTS_DIR     = ROOT_DIR / "ml" / "artifacts"
DATABASE_DIR      = ROOT_DIR / "database"

TRAINING_DATA_PATH    = DATA_DIR / "training_data.csv"
INCIDENTS_DATA_PATH   = DATA_DIR / "historical_incidents.csv"
SAMPLE_BATCH_PATH     = DATA_DIR / "sample_batch_input.csv"
MODEL_PATH            = MODEL_DIR / "landslide_model.pkl"
SCALER_PATH           = MODEL_DIR / "scaler.pkl"
FEATURE_COLS_PATH     = MODEL_DIR / "feature_columns.json"
DB_PATH               = DATABASE_DIR / "predictions.db"

# ── Risk level mapping ────────────────────────────────────────────────────────
RISK_LABELS = {
    0: "Low",
    1: "Moderate",
    2: "High",
    3: "Very High",
}

RISK_COLORS = {
    "Low":       "#2ecc71",   # green
    "Moderate":  "#f1c40f",   # yellow
    "High":      "#e67e22",   # orange
    "Very High": "#e74c3c",   # red
}

RISK_EMOJIS = {
    "Low":       "🟢",
    "Moderate":  "🟡",
    "High":      "🟠",
    "Very High": "🔴",
}

# Risk code at which an alert is triggered (2 = High, 3 = Very High)
ALERT_THRESHOLD = 2

# ── Feature definitions ───────────────────────────────────────────────────────
# These are the columns the ML model expects (in this exact order).
FEATURE_COLUMNS = [
    "rainfall_mm",
    "soil_moisture_pct",
    "slope_angle_deg",
    "ndvi",
    "lithology_code",
]

# ── Input validation ranges ───────────────────────────────────────────────────
VALID_RANGES = {
    "latitude":          (21.0,  29.5),
    "longitude":         (88.0,  97.5),
    "rainfall_mm":       (0.0,   600.0),
    "soil_moisture_pct": (0.0,   100.0),
    "slope_angle_deg":   (0.0,   80.0),
    "ndvi":              (-1.0,  1.0),
    "lithology_code":    (1,     5),
}

# ── NER map settings ──────────────────────────────────────────────────────────
MAP_CENTER      = [25.5, 92.0]   # approximate centre of North Eastern Region
MAP_ZOOM        = 6
NER_STATES      = [
    "Assam", "Meghalaya", "Nagaland", "Manipur",
    "Mizoram", "Tripura", "Arunachal Pradesh", "Sikkim",
]

# ── Prototype disclaimer (shown everywhere) ───────────────────────────────────
DISCLAIMER = (
    "⚠️ PROTOTYPE ONLY — SIH26001 Student Demonstration. "
    "This system uses historical and simulated data. "
    "It is NOT an official disaster-warning system. "
    "Do not use for emergency decisions."
)

# ── Email / alert settings (loaded from .env at runtime) ─────────────────────
EMAIL_SENDER    = os.getenv("ALERT_EMAIL_SENDER", "")
EMAIL_PASSWORD  = os.getenv("ALERT_EMAIL_PASSWORD", "")
EMAIL_RECIPIENT = os.getenv("ALERT_EMAIL_RECIPIENT", "")
SMTP_HOST       = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT       = int(os.getenv("SMTP_PORT", "587"))

# ── Flask API settings ────────────────────────────────────────────────────────
FLASK_HOST  = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT  = int(os.getenv("FLASK_PORT", "5000"))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
