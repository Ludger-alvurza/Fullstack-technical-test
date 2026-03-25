"""
ML Model singleton loader untuk digunakan backend.
"""

import sys
import os

# Tambahkan direktori ml ke Python path agar bisa import
# Lokasi file ini: backend/core/ml_model.py
# ML dir ada di: <project_root>/ml → naik 3 level (core → backend → project_root)
ML_DIR = os.path.join(
    os.path.dirname(  # project_root
        os.path.dirname(  # backend/
            os.path.dirname(os.path.abspath(__file__))  # backend/core/
        )
    ),
    "ml"
)
if ML_DIR not in sys.path:
    sys.path.insert(0, ML_DIR)

from predict import load_model, predict as ml_predict  # noqa: E402


def get_prediction(jumlah_penjualan: float, harga: float, diskon: float) -> dict:
    """
    Wrapper untuk memanggil ML predict dan return dict response.
    """
    status, confidence = ml_predict(jumlah_penjualan, harga, diskon)
    return {
        "status": status,
        "confidence": round(confidence * 100, 2),
        "label": "Laris ✅" if status == "Laris" else "Tidak Laris ❌",
    }


# Pre-load model saat modul di-import (startup)
try:
    load_model()
    print("[ML] ✅ Model berhasil dimuat saat startup.")
except FileNotFoundError as e:
    print(f"[ML] ⚠️  {e}")
