import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import SalesTable from '../components/SalesTable';
import PredictForm from '../components/PredictForm';

export default function DashboardPage() {
  const navigate = useNavigate();
  const userInfo = JSON.parse(localStorage.getItem('user_info') || '{}');

  const [sales, setSales] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [activeTab, setActiveTab] = useState('sales'); // 'sales' | 'predict'

  const fetchSales = useCallback(async () => {
    setLoading(true);
    try {
      const params = { limit: 200 };
      if (statusFilter) params.status = statusFilter;
      if (search) params.search = search;
      const res = await api.get('/sales', { params });
      setSales(res.data.data);
      setTotal(res.data.total);
    } catch {
      // 401 handled by interceptor
    } finally {
      setLoading(false);
    }
  }, [search, statusFilter]);

  useEffect(() => {
    fetchSales();
  }, [fetchSales]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
    navigate('/login');
  };

  // Derived stats
  const larisCount = sales.filter((s) => s.status === 'Laris').length;
  const tidakCount = sales.filter((s) => s.status !== 'Laris').length;
  const avgHarga = sales.length
    ? Math.round(sales.reduce((a, b) => a + b.harga, 0) / sales.length)
    : 0;

  return (
    <div className="dashboard">
      {/* ── Navbar ─────────────────────────────────────────────────── */}
      <header className="navbar">
        <div className="navbar-brand">
          <span className="brand-icon">📊</span>
          <span>Sales Prediction</span>
        </div>
        <div className="navbar-right">
          <span className="navbar-user">👤 {userInfo.full_name || userInfo.username}</span>
          <button className="btn-ghost btn-sm" id="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard-main">
        {/* ── Stats Cards ─────────────────────────────────────────── */}
        <section className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">{total}</div>
            <div className="stat-label">Total Produk</div>
          </div>
          <div className="stat-card stat-laris">
            <div className="stat-value">{larisCount}</div>
            <div className="stat-label">✅ Laris</div>
          </div>
          <div className="stat-card stat-tidak">
            <div className="stat-value">{tidakCount}</div>
            <div className="stat-label">❌ Tidak Laris</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">
              {avgHarga.toLocaleString('id-ID', {
                style: 'currency',
                currency: 'IDR',
                maximumFractionDigits: 0,
              })}
            </div>
            <div className="stat-label">Rata-rata Harga</div>
          </div>
        </section>

        {/* ── Tabs ────────────────────────────────────────────────── */}
        <div className="tabs">
          <button
            className={`tab-btn ${activeTab === 'sales' ? 'tab-active' : ''}`}
            id="tab-sales"
            onClick={() => setActiveTab('sales')}
          >
            📋 Data Penjualan
          </button>
          <button
            className={`tab-btn ${activeTab === 'predict' ? 'tab-active' : ''}`}
            id="tab-predict"
            onClick={() => setActiveTab('predict')}
          >
            🤖 Prediksi Produk
          </button>
        </div>

        {/* ── Sales Tab ───────────────────────────────────────────── */}
        {activeTab === 'sales' && (
          <section className="sales-section">
            <div className="section-toolbar">
              <input
                type="text"
                id="search-input"
                className="search-input"
                placeholder="🔍 Cari nama produk..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              <select
                id="status-filter"
                className="select-filter"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="">Semua Status</option>
                <option value="Laris">✅ Laris</option>
                <option value="Tidak">❌ Tidak Laris</option>
              </select>
              <button className="btn-ghost btn-sm" id="refresh-btn" onClick={fetchSales}>
                🔄 Refresh
              </button>
            </div>
            <SalesTable data={sales} loading={loading} />
          </section>
        )}

        {/* ── Predict Tab ─────────────────────────────────────────── */}
        {activeTab === 'predict' && <PredictForm />}
      </main>
    </div>
  );
}
