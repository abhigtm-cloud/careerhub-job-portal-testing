import { useEffect, useState } from 'react';
import { api } from '../api/client';
import Loading from '../components/Loading.jsx';
import EmptyState from '../components/EmptyState.jsx';

const STATUS_LABELS = {
  submitted: 'Submitted',
  under_review: 'Under review',
  shortlisted: 'Shortlisted',
  rejected: 'Rejected',
  hired: 'Hired'
};

export default function MyApplicationsPage() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/applications/mine')
      .then((data) => setApplications(data.applications))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loading label="Loading your applications..." />;

  return (
    <div className="container py-4">
      <h3 className="mb-4">My Applications</h3>
      {applications.length === 0 ? (
        <EmptyState title="No applications yet" subtitle="Browse jobs and apply to see them here." />
      ) : (
        <div data-testid="applications-list">
          {applications.map((app) => (
            <div key={app._id} className="dashboard-card mb-3" data-testid="application-item">
              <div className="d-flex justify-content-between">
                <div>
                  <h5>{app.job?.title || 'Job removed'}</h5>
                  <div className="text-muted">{app.job?.company}</div>
                </div>
                <span className="badge text-bg-light border" data-testid="application-status">
                  {STATUS_LABELS[app.status] || app.status}
                </span>
              </div>
              <div className="text-muted small mt-2">
                Applied on {new Date(app.createdAt).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
