"""
ML Inference Module - Sales Prediction System
Load model dan expose fungsi prediksi untuk digunakan backend.
"""

import os
import joblib
import numpy as np
from typing import Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model/sales_model.joblib")

# Singleton model instance
_model = None


def load_model():
    """Load model dari file joblib (singleton pattern)."""
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file tidak ditemukan: {MODEL_PATH}\n"
                "Jalankan dulu: python ml/train_model.py"
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def predict(
    jumlah_penjualan: float, harga: float, diskon: float
) -> Tuple[str, float]:
    """
    Prediksi status produk.

    Args:
        jumlah_penjualan: Jumlah unit terjual
        harga: Harga satuan per item (Rupiah)
        diskon: Persentase diskon (0-100)

    Returns:
        Tuple (status, confidence)
        - status: "Laris" atau "Tidak"
        - confidence: probabilitas kelas prediksi (0.0 - 1.0)
    """
    model = load_model()
    import pandas as pd
    features = pd.DataFrame(
        [[jumlah_penjualan, harga, diskon]],
        columns=["jumlah_penjualan", "harga", "diskon"],
    )

    # Predict class dan probabilitas
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    status = "Laris" if prediction == 1 else "Tidak"
    confidence = float(probabilities[prediction])

    return status, confidence
