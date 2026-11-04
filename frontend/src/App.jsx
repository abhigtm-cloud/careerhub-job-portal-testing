import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar.jsx';
import ProtectedRoute from './components/ProtectedRoute.jsx';
import JobsPage from './pages/JobsPage.jsx';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import MyApplicationsPage from './pages/MyApplicationsPage.jsx';
import SavedJobsPage from './pages/SavedJobsPage.jsx';
import ProfilePage from './pages/ProfilePage.jsx';
import RecruiterDashboardPage from './pages/RecruiterDashboardPage.jsx';

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<JobsPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/applications"
          element={<ProtectedRoute role="candidate"><MyApplicationsPage /></ProtectedRoute>}
        />
        <Route
          path="/saved-jobs"
          element={<ProtectedRoute role="candidate"><SavedJobsPage /></ProtectedRoute>}
        />
        <Route
          path="/profile"
          element={<ProtectedRoute role="candidate"><ProfilePage /></ProtectedRoute>}
        />
        <Route
          path="/recruiter"
          element={<ProtectedRoute role="recruiter"><RecruiterDashboardPage /></ProtectedRoute>}
        />
      </Routes>
    </>
  );
}
