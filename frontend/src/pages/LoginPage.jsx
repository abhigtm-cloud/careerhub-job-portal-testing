import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import { useToast } from '../context/ToastContext.jsx';

export default function LoginPage() {
  const { login } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      const user = await login(email, password);
      showToast(`Welcome back, ${user.name}`, 'success');
      navigate(user.role === 'recruiter' ? '/recruiter' : '/');
    } catch (err) {
      setError(err.message || 'Login failed');
    } finally {
      setSubmitting(false);
    }
  }

  async function demoLogin(role) {
    setError('');
    setSubmitting(true);
    try {
      const demoEmail = role === 'candidate' ? 'candidate@careerhub.com' : 'recruiter@careerhub.com';
      const user = await login(demoEmail, 'CareerHub@123');
      showToast(`Logged in as demo ${role}`, 'success');
      navigate(role === 'recruiter' ? '/recruiter' : '/');
    } catch (err) {
      setError('Demo login failed. Has the database been seeded?');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="container">
      <div className="auth-card" data-testid="login-card">
        <h3 className="mb-3">Log in to CareerHub</h3>
        <form onSubmit={handleSubmit} data-testid="login-form" noValidate>
          <label className="form-label">Email</label>
          <input
            type="email"
            className="form-control mb-3"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            data-testid="input-email"
            required
          />
          <label className="form-label">Password</label>
          <input
            type="password"
            className="form-control mb-3"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            data-testid="input-password"
            required
          />
          {error && <div className="alert alert-danger py-2" data-testid="login-error">{error}</div>}
          <button type="submit" className="btn btn-ch-primary w-100 mb-2" disabled={submitting} data-testid="btn-login">
            {submitting ? 'Logging in...' : 'Log in'}
          </button>
        </form>

        <div className="d-flex gap-2 mt-2">
          <button className="btn btn-outline-secondary btn-sm w-50" onClick={() => demoLogin('candidate')} data-testid="btn-demo-candidate">
            Demo candidate
          </button>
          <button className="btn btn-outline-secondary btn-sm w-50" onClick={() => demoLogin('recruiter')} data-testid="btn-demo-recruiter">
            Demo recruiter
          </button>
        </div>

        <p className="text-center mt-3 mb-0">
          Don&apos;t have an account? <Link to="/register" data-testid="link-register">Sign up</Link>
        </p>
      </div>
    </div>
  );
}
