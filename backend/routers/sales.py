"""
Router: Sales Data
GET /sales → daftar data penjualan dari CSV (protected by JWT)
"""

from typing import List, Optional

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from core.config import DATA_CSV_PATH
from core.security import verify_token

router = APIRouter(tags=["Sales"])


class SalesItem(BaseModel):
    product_id: str
    product_name: str
    jumlah_penjualan: int
    harga: float
    diskon: float
    status: str


class SalesResponse(BaseModel):
    total: int
    data: List[SalesItem]


def _load_csv() -> pd.DataFrame:
    """Load dan validasi CSV file."""
    try:
        df = pd.read_csv(DATA_CSV_PATH)
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File data tidak ditemukan: {DATA_CSV_PATH}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal membaca data: {str(e)}",
        )


@router.get(
    "/sales",
    response_model=SalesResponse,
    summary="Ambil data penjualan",
    description=(
        "Mengembalikan seluruh data penjualan dari CSV.\n\n"
        "**Filter opsional:**\n"
        "- `status`: filter berdasarkan status (`Laris` / `Tidak`)\n"
        "- `search`: cari berdasarkan nama produk\n"
        "- `limit` / `offset`: pagination"
    ),
)
def get_sales(
    status_filter: Optional[str] = Query(
        None, alias="status", description="Filter: 'Laris' atau 'Tidak'"
    ),
    search: Optional[str] = Query(None, description="Cari nama produk"),
    limit: int = Query(100, ge=1, le=500, description="Jumlah data per halaman"),
    offset: int = Query(0, ge=0, description="Offset pagination"),
    _: dict = Depends(verify_token),
) -> SalesResponse:
    df = _load_csv()

    # Filter status
    if status_filter:
        df = df[df["status"].str.strip() == status_filter.strip()]

    # Search nama produk
    if search:
        df = df[df["product_name"].str.contains(search, case=False, na=False)]

    total = len(df)
    df_page = df.iloc[offset : offset + limit]

    items = [
        SalesItem(
            product_id=str(row["product_id"]),
            product_name=str(row["product_name"]),
            jumlah_penjualan=int(row["jumlah_penjualan"]),
            harga=float(row["harga"]),
            diskon=float(row["diskon"]),
            status=str(row["status"]).strip(),
        )
        for _, row in df_page.iterrows()
    ]

    return SalesResponse(total=total, data=items)
