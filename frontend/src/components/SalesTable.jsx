export default function SalesTable({ data, loading }) {
  if (loading) {
    return (
      <div className="table-loading">
        <div className="spinner large" />
        <p>Memuat data penjualan...</p>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return <p className="table-empty">Tidak ada data ditemukan.</p>;
  }

  return (
    <div className="table-wrapper">
      <table className="sales-table" id="sales-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Produk</th>
            <th>Jml. Penjualan</th>
            <th>Harga</th>
            <th>Diskon</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, idx) => (
            <tr key={item.product_id}>
              <td className="td-num">{idx + 1}</td>
              <td className="td-name">{item.product_name}</td>
              <td className="td-num">{item.jumlah_penjualan.toLocaleString('id-ID')}</td>
              <td className="td-num">
                {item.harga.toLocaleString('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 })}
              </td>
              <td className="td-num">{item.diskon}%</td>
              <td>
                <span className={`badge ${item.status === 'Laris' ? 'badge-laris' : 'badge-tidak'}`}>
                  {item.status === 'Laris' ? '✅ Laris' : '❌ Tidak'}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
