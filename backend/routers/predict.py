"""
Router: ML Prediction
POST /predict → prediksi status produk (Laris / Tidak) via ML model
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from core.ml_model import get_prediction
from core.security import verify_token

router = APIRouter(tags=["Prediction"])


class PredictRequest(BaseModel):
    jumlah_penjualan: float = Field(
        ..., ge=0, description="Jumlah unit terjual", example=500
    )
    harga: float = Field(
        ..., ge=0, description="Harga satuan per item (Rupiah)", example=150000
    )
    diskon: float = Field(
        ..., ge=0, le=100, description="Persentase diskon (0-100)", example=10
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "jumlah_penjualan": 500,
                    "harga": 150000,
                    "diskon": 10,
                }
            ]
        }
    }


class PredictResponse(BaseModel):
    status: str
    label: str
    confidence: float
    input: PredictRequest


@router.post(
    "/predict",
    response_model=PredictResponse,
    summary="Prediksi status produk",
    description=(
        "Prediksi apakah produk termasuk **Laris** atau **Tidak Laris** "
        "berdasarkan jumlah penjualan, harga, dan diskon.\n\n"
        "Menggunakan model **Random Forest** yang telah dilatih sebelumnya."
    ),
)
def predict_product(
    body: PredictRequest,
    _: dict = Depends(verify_token),
) -> PredictResponse:
    try:
        result = get_prediction(
            jumlah_penjualan=body.jumlah_penjualan,
            harga=body.harga,
            diskon=body.diskon,
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal melakukan prediksi: {str(e)}",
        )

    return PredictResponse(
        status=result["status"],
        label=result["label"],
        confidence=result["confidence"],
        input=body,
    )
