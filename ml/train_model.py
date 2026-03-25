"""
ML Training Script - Sales Prediction System
Train Random Forest Classifier untuk prediksi status produk (Laris / Tidak)
"""

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/sales_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model/sales_model.joblib")


def load_data(path: str) -> pd.DataFrame:
    """Load dan validasi dataset CSV."""
    df = pd.read_csv(path)
    required_cols = {"jumlah_penjualan", "harga", "diskon", "status"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Kolom yang dibutuhkan tidak ada: {missing}")
    return df


def preprocess(df: pd.DataFrame):
    """
    Preprocessing:
    - Pilih fitur: jumlah_penjualan, harga, diskon
    - Encode label: Laris → 1, Tidak → 0
    - Return X, y
    """
    features = ["jumlah_penjualan", "harga", "diskon"]
    X = df[features].copy()

    # Hapus row dengan NaN
    df_clean = df.dropna(subset=features + ["status"])
    X = df_clean[features].copy()

    # Normalisasi nama status
    df_clean = df_clean.copy()
    df_clean["status"] = df_clean["status"].str.strip()
    y = (df_clean["status"] == "Laris").astype(int)

    print(f"[INFO] Dataset shape: {X.shape}")
    print(f"[INFO] Distribusi label:\n{df_clean['status'].value_counts()}\n")
    return X, y


def train(X, y):
    """Train Random Forest Classifier dan evaluasi."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    # Evaluasi
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("=" * 50)
    print("📊  EVALUASI MODEL")
    print("=" * 50)
    print(f"Accuracy  : {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("\nClassification Report:")
    print(
        classification_report(
            y_test, y_pred, target_names=["Tidak Laris", "Laris"]
        )
    )
    print("=" * 50)

    # Feature importance
    importances = model.feature_importances_
    feature_names = X.columns.tolist()
    print("\n📌 Feature Importance:")
    for name, imp in sorted(
        zip(feature_names, importances), key=lambda x: -x[1]
    ):
        print(f"   {name}: {imp:.4f}")

    return model, accuracy


def save_model(model, path: str):
    """Simpan model ke file joblib."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"\n✅  Model disimpan ke: {path}")


if __name__ == "__main__":
    print("🚀  Memulai training model...\n")
    df = load_data(DATA_PATH)
    X, y = preprocess(df)
    model, accuracy = train(X, y)
    save_model(model, MODEL_PATH)
    print(f"\n🎉  Training selesai! Accuracy: {accuracy*100:.2f}%")
