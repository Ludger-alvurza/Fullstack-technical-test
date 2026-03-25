import { useState } from 'react';
import api from '../api/axios';

const initialForm = { jumlah_penjualan: '', harga: '', diskon: '' };

export default function PredictForm() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);
    try {
      const payload = {
        jumlah_penjualan: parseFloat(form.jumlah_penjualan),
        harga: parseFloat(form.harga),
        diskon: parseFloat(form.diskon),
      };
      const res = await api.post('/predict', payload);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediksi gagal. Coba lagi.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setForm(initialForm);
    setResult(null);
    setError('');
  };

  return (
    <div className="predict-card" id="predict-form-section">
      <div className="predict-header">
        <h3>🤖 Prediksi Status Produk</h3>
        <p>Masukkan data produk untuk memprediksi apakah produk akan <strong>Laris</strong> atau <strong>Tidak</strong>.</p>
      </div>

      <form onSubmit={handleSubmit} className="predict-form" id="predict-form">
        <div className="predict-inputs">
          <div className="form-group">
            <label htmlFor="jumlah_penjualan">Jumlah Penjualan (unit)</label>
            <input
              id="jumlah_penjualan"
              name="jumlah_penjualan"
              type="number"
              min="0"
              placeholder="contoh: 500"
              value={form.jumlah_penjualan}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="harga">Harga Satuan (Rp)</label>
            <input
              id="harga"
              name="harga"
              type="number"
              min="0"
              placeholder="contoh: 150000"
              value={form.harga}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="diskon">Diskon (%)</label>
            <input
              id="diskon"
              name="diskon"
              type="number"
              min="0"
              max="100"
              placeholder="contoh: 10"
              value={form.diskon}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="predict-actions">
          <button type="submit" className="btn-primary" id="predict-submit" disabled={loading}>
            {loading ? <><span className="spinner" /> Memprediksi...</> : '🔮 Prediksi Sekarang'}
          </button>
          <button type="button" className="btn-ghost" onClick={handleReset}>Reset</button>
        </div>
      </form>

      {error && <div className="alert-error">{error}</div>}

      {result && (
        <div className={`predict-result ${result.status === 'Laris' ? 'result-laris' : 'result-tidak'}`} id="predict-result">
          <div className="result-label">{result.label}</div>
          <div className="result-meta">
            <div className="result-meta-item">
              <span>Confidence</span>
              <strong>{result.confidence}%</strong>
            </div>
            <div className="result-meta-item">
              <span>Jumlah Penjualan</span>
              <strong>{parseInt(result.input.jumlah_penjualan).toLocaleString('id-ID')} unit</strong>
            </div>
            <div className="result-meta-item">
              <span>Harga</span>
              <strong>
                {parseFloat(result.input.harga).toLocaleString('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 })}
              </strong>
            </div>
            <div className="result-meta-item">
              <span>Diskon</span>
              <strong>{result.input.diskon}%</strong>
            </div>
          </div>
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{ width: `${result.confidence}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
