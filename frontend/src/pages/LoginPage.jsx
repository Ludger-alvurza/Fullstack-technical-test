import { useState } from 'react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await api.post('/login', form);
      localStorage.setItem('access_token', res.data.access_token);
      localStorage.setItem('user_info', JSON.stringify({
        username: res.data.username,
        full_name: res.data.full_name,
      }));
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login gagal. Coba lagi.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-bg">
      <div className="login-card">
        {/* Logo / Icon */}
        <div className="login-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 3h18v18H3z" rx="2"/>
            <path d="M3 9h18M9 21V9"/>
          </svg>
        </div>

        <h1 className="login-title">Sales Prediction</h1>
        <p className="login-subtitle">Mini AI System – Masuk untuk melanjutkan</p>

        <form onSubmit={handleSubmit} className="login-form" id="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              placeholder="admin"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
              required
              autoFocus
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
            />
          </div>

          {error && <div className="alert-error" role="alert">{error}</div>}

          <button
            type="submit"
            className="btn-primary btn-block"
            id="login-submit"
            disabled={loading}
          >
            {loading ? <span className="spinner" /> : 'Masuk'}
          </button>
        </form>

        <p className="login-hint">
          Demo: <strong>admin</strong> / <strong>admin123</strong>
        </p>
      </div>
    </div>
  );
}
