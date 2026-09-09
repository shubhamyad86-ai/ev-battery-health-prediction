import joblib
import numpy as np
import pandas as pd

try:
    from .config import BEST_MODEL, FALLBACK_MODEL, SCALER_FILE, FEATURE_COLUMNS
except ImportError:
    from config import BEST_MODEL, FALLBACK_MODEL, SCALER_FILE, FEATURE_COLUMNS


class BatteryPredictor:

    def __init__(self):
        # Prefer best_model.pkl (whichever model actually won the
        # training comparison in train_model.py). Fall back to
        # linear_regression.pkl only if best_model.pkl hasn't been
        # generated yet, so the predictor still works out of the box.
        if BEST_MODEL.exists():
            self.model = joblib.load(BEST_MODEL)
        elif FALLBACK_MODEL.exists():
            self.model = joblib.load(FALLBACK_MODEL)
        else:
            raise FileNotFoundError(
                f"No trained model found. Expected {BEST_MODEL} or {FALLBACK_MODEL}. "
                "Run src/train_model.py first."
            )

        self.scaler = joblib.load(SCALER_FILE)
        self.feature_names = FEATURE_COLUMNS

    def predict(self, features):

        # Single prediction
        if isinstance(features, (list, tuple, np.ndarray)):
            features = pd.DataFrame([features], columns=self.feature_names)

        # Batch prediction
        elif isinstance(features, pd.DataFrame):
            missing = [c for c in self.feature_names if c not in features.columns]
            if missing:
                raise ValueError(f"Input is missing required columns: {missing}")
            features = features[self.feature_names]

        else:
            raise ValueError("Input must be a list, tuple, numpy array, or pandas DataFrame.")

        features_scaled = self.scaler.transform(features)

        predictions = self.model.predict(features_scaled)
        predictions = np.clip(predictions, 0, 100)

        if len(predictions) == 1:
            return float(predictions[0])

        return predictions
