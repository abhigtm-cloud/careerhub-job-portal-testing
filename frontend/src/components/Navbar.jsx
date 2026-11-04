import { Link, useNavigate } from 'react-router-dom';
import { Briefcase, LogOut, LayoutDashboard, User as UserIcon } from 'lucide-react';
import { useAuth } from '../context/AuthContext.jsx';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate('/login');
  }

  return (
    <nav className="navbar navbar-expand-lg navbar-ch sticky-top" data-testid="navbar">
      <div className="container">
        <Link className="navbar-brand brand d-flex align-items-center gap-2" to="/">
          <Briefcase size={22} /> CareerHub
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarMain"
          aria-controls="navbarMain"
          aria-expanded="false"
          aria-label="Toggle navigation"
          data-testid="navbar-toggler"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse justify-content-end" id="navbarMain" data-testid="navbar-collapse">
          <ul className="navbar-nav align-items-lg-center gap-2">
            <li className="nav-item">
              <Link className="nav-link" to="/" data-testid="nav-jobs">Jobs</Link>
            </li>
            {user && user.role === 'candidate' && (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/applications" data-testid="nav-applications">My Applications</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/saved-jobs" data-testid="nav-saved-jobs">Saved Jobs</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/profile" data-testid="nav-profile">
                    <UserIcon size={16} className="me-1" /> Profile
                  </Link>
                </li>
              </>
            )}
            {user && user.role === 'recruiter' && (
              <li className="nav-item">
                <Link className="nav-link" to="/recruiter" data-testid="nav-recruiter-dashboard">
                  <LayoutDashboard size={16} className="me-1" /> Dashboard
                </Link>
              </li>
            )}
            {!user && (
              <>
                <li className="nav-item">
                  <Link className="btn btn-outline-primary btn-sm" to="/login" data-testid="nav-login">
                    Log in
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="btn btn-ch-primary btn-sm" to="/register" data-testid="nav-register">
                    Sign up
                  </Link>
                </li>
              </>
            )}
            {user && (
              <li className="nav-item">
                <button className="btn btn-outline-secondary btn-sm" onClick={handleLogout} data-testid="nav-logout">
                  <LogOut size={14} className="me-1" /> Logout
                </button>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}
