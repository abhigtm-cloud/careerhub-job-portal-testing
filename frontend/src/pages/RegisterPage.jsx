import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import { useToast } from '../context/ToastContext.jsx';

export default function RegisterPage() {
  const { register } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'candidate', company: '' });
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  function update(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');

    if (form.name.trim().length < 2) return setError('Name must be at least 2 characters');
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) return setError('Enter a valid email address');
    if (form.password.length < 6) return setError('Password must be at least 6 characters');

    setSubmitting(true);
    try {
      const user = await register(form);
      showToast(`Welcome to CareerHub, ${user.name}`, 'success');
      navigate(user.role === 'recruiter' ? '/recruiter' : '/');
    } catch (err) {
      setError(err.message || 'Registration failed');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="container">
      <div className="auth-card" data-testid="register-card">
        <h3 className="mb-3">Create your account</h3>
        <form onSubmit={handleSubmit} data-testid="register-form" noValidate>
          <label className="form-label">I am a</label>
          <select
            className="form-select mb-3"
            value={form.role}
            onChange={(e) => update('role', e.target.value)}
            data-testid="select-role"
          >
            <option value="candidate">Candidate</option>
            <option value="recruiter">Recruiter</option>
          </select>

          <label className="form-label">Full name</label>
          <input
            className="form-control mb-3"
            value={form.name}
            onChange={(e) => update('name', e.target.value)}
            data-testid="input-name"
            required
          />

          {form.role === 'recruiter' && (
            <>
              <label className="form-label">Company</label>
              <input
                className="form-control mb-3"
                value={form.company}
                onChange={(e) => update('company', e.target.value)}
                data-testid="input-company"
              />
            </>
          )}

          <label className="form-label">Email</label>
          <input
            type="email"
            className="form-control mb-3"
            value={form.email}
            onChange={(e) => update('email', e.target.value)}
            data-testid="input-email"
            required
          />

          <label className="form-label">Password</label>
          <input
            type="password"
            className="form-control mb-3"
            value={form.password}
            onChange={(e) => update('password', e.target.value)}
            data-testid="input-password"
            required
          />

          {error && <div className="alert alert-danger py-2" data-testid="register-error">{error}</div>}

          <button type="submit" className="btn btn-ch-primary w-100" disabled={submitting} data-testid="btn-register">
            {submitting ? 'Creating account...' : 'Sign up'}
          </button>
        </form>
        <p className="text-center mt-3 mb-0">
          Already have an account? <Link to="/login" data-testid="link-login">Log in</Link>
        </p>
      </div>
    </div>
  );
}
