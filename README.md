# Mini AI Sales Prediction System

Sistem fullstack untuk mengelola dan memprediksi status penjualan produk menggunakan Machine Learning.

## Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────┐
│                      FRONTEND                           │
│              React + Vite (Port 5173)                   │
│   Login Page │ Dashboard │ Sales Table │ Predict Form   │
└────────────────────────┬────────────────────────────────┘
                         │ REST API (HTTP + JWT)
┌────────────────────────▼────────────────────────────────┐
│                      BACKEND                            │
│              FastAPI (Port 8000)                        │
│   POST /login │ GET /sales │ POST /predict              │
│                     │                                   │
│         ┌───────────┴──────────┐                        │
│         ▼                      ▼                        │
│   data/sales_data.csv    ml/model/sales_model.joblib    │
│   (Data Source)          (ML Model - Random Forest)     │
└─────────────────────────────────────────────────────────┘
```

**Alur Data:**
1. User login → dapat JWT token
2. Frontend kirim token di setiap request (Bearer)
3. Backend baca CSV → return data penjualan
4. Backend load ML model → return prediksi status produk

## Cara Menjalankan

### Prasyarat
- Python 3.10+
- Node.js 18+

### 1. Clone & Persiapan

```bash
git clone <repo-url>
cd "Fullstack Technical Test"
```

### 2. Backend (Terminal 1)

```bash
# Buat virtual environment
python3 -m venv venv
source venv/bin/activate       # Linux/Mac
# venv\Scripts\activate        # Windows

# Install dependencies
pip install -r backend/requirements.txt

# Train ML model (wajib sebelum menjalankan backend)
python ml/train_model.py

# Jalankan backend
cd backend
uvicorn main:app --reload --port 8000
```

Backend aktif di → **http://localhost:8000**
Swagger API Docs → **http://localhost:8000/docs**

### 3. Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

Frontend aktif di → **http://localhost:5173**

### 4. Login

| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | admin123  | Admin |
| user     | user123   | Viewer|

---

## Struktur Project

```
Fullstack Technical Test/
├── data/
│   └── sales_data.csv          # Dataset 5.000 produk (product_id format P00001)
├── ml/
│   ├── train_model.py          # Script training Random Forest
│   ├── predict.py              # Inference module
│   └── model/
│       └── sales_model.joblib  # Model tersimpan (auto-generated)
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── requirements.txt
│   ├── core/
│   │   ├── config.py           # Konfigurasi & dummy users
│   │   ├── security.py         # JWT utilities
│   │   └── ml_model.py         # ML loader untuk backend
│   └── routers/
│       ├── auth.py             # POST /login
│       ├── sales.py            # GET /sales
│       └── predict.py          # POST /predict
├── frontend/
│   ├── src/
│   │   ├── api/axios.js        # Axios + JWT interceptor
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   └── DashboardPage.jsx
│   │   └── components/
│   │       ├── SalesTable.jsx
│   │       ├── PredictForm.jsx
│   │       └── PrivateRoute.jsx
│   └── vite.config.js
└── README.md
```

---

## API Endpoints

| Method | Endpoint   | Auth | Deskripsi                        |
|--------|------------|------|----------------------------------|
| POST   | `/login`   | ❌   | Login, return JWT token          |
| GET    | `/sales`   | ✅   | Ambil data penjualan dari CSV    |
| POST   | `/predict` | ✅   | Prediksi status produk via ML    |
| GET    | `/`        | ❌   | Health check                     |

### Contoh POST /predict

```json
// Request
{
  "jumlah_penjualan": 500,
  "harga": 150000,
  "diskon": 10
}

// Response
{
  "status": "Laris",
  "label": "Laris ✅",
  "confidence": 96.0,
  "input": { ... }
}
```

---

## Design Decisions

### Machine Learning
- **Model:** Random Forest Classifier (100 estimators) — dipilih karena robust terhadap outlier, tidak perlu feature scaling, dan memberikan feature importance yang interpretatif.
- **Features:** `jumlah_penjualan` (dominan, 98.8%), `harga` (1.0%), `diskon` (0.2%).
- **Dataset:** 5.000 baris, `product_id` format string (`P00001`), 3.608 Laris / 1.392 Tidak.
- **Accuracy:** **100%** pada test set (1.000 samples, stratified split 80/20).
- **Persistence:** Disimpan dengan `joblib` sebagai `.joblib` file, dimuat saat backend startup (singleton pattern).

### Backend
- **FastAPI** dipilih karena auto-generate Swagger docs, async-ready, dan Pydantic validation bawaan.
- **JWT** menggunakan `python-jose` dengan HS256. Dummy user disimpan di config (production: ganti dengan DB + hashed password).
- **CORS** dibuka untuk semua origin di dev mode. Di production, restrict ke domain spesifik.
- **Error handling:** HTTP 401 untuk auth, 503 jika model belum ditraining, 500 untuk error internal.

### Frontend
- **React + Vite** untuk DX yang cepat.
- **Axios interceptor** menangani Token Injection dan redirect otomatis ke login jika 401.
- **Vite proxy** digunakan saat dev agar tidak perlu CORS preflight.
- State management: local state (`useState`) cukup untuk skala project ini.

## Asumsi

1. Dataset `sales_data.csv` berisi 5.000 baris data sintetik; `product_id` berformat string (`P00001`).
2. `jumlah_penjualan` adalah fitur terpenting (98.8%) — threshold ~100 unit menentukan Laris/Tidak.
3. Authentication menggunakan dummy user hardcoded; cukup untuk scope technical test.
4. Tidak ada deployment ke cloud — dijalankan secara lokal sesuai instruksi.
5. `diskon` berpengaruh sangat kecil terhadap prediksi dibanding volume penjualan.
