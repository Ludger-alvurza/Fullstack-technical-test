"""
Mini AI Sales Prediction System – Backend Entry Point
FastAPI application dengan JWT authentication dan ML integration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, sales, predict

# ── App Init ───────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Sales Prediction API",
    description=(
        "**Mini AI Sales Prediction System**\n\n"
        "REST API untuk:\n"
        "- 🔐 **Authentication** – JWT-based login\n"
        "- 📊 **Sales Data** – Ambil & filter data penjualan\n"
        "- 🤖 **Prediction** – Prediksi status produk via Machine Learning\n\n"
        "**Dummy credentials:** `admin / admin123` atau `user / user123`\n\n"
        "Gunakan `POST /login` untuk mendapatkan token, kemudian klik **Authorize** "
        "dan masukkan token sebagai `Bearer <token>`."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS Middleware ────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Untuk dev; restrict di production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(sales.router)
app.include_router(predict.router)


# ── Health Check ───────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"], summary="Health check")
def root():
    return {
        "status": "ok",
        "message": "Sales Prediction API is running 🚀",
        "docs": "/docs",
    }
