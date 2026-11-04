import { useState } from 'react';
import { X } from 'lucide-react';
import { useAuth } from '../context/AuthContext.jsx';
import { useToast } from '../context/ToastContext.jsx';
import { api } from '../api/client';

export default function JobDetailModal({ job, onClose, onApplied }) {
  const { user } = useAuth();
  const { showToast } = useToast();
  const [coverLetter, setCoverLetter] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  if (!job) return null;

  async function handleApply(e) {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await api.post('/applications', { jobId: job._id, coverLetter });
      showToast('Application submitted successfully', 'success');
      onApplied && onApplied(job);
      onClose();
    } catch (err) {
      if (err.status === 409) {
        setError('You have already applied to this job.');
      } else {
        setError(err.message || 'Failed to submit application');
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="modal-backdrop-custom" data-testid="job-detail-modal" style={backdropStyle}>
      <div className="modal-content-custom" style={modalStyle}>
        <div className="d-flex justify-content-between align-items-start mb-3">
          <div>
            <h4 data-testid="modal-job-title">{job.title}</h4>
            <div className="text-muted">{job.company} &middot; {job.location}</div>
          </div>
          <button className="btn btn-sm btn-light" onClick={onClose} data-testid="btn-close-modal" aria-label="Close">
            <X size={18} />
          </button>
        </div>

        <div className="mb-3">
          {(job.skills || []).map((s) => <span key={s} className="badge-skill">{s}</span>)}
        </div>

        <p data-testid="modal-job-description">{job.description}</p>

        {job.requirements && job.requirements.length > 0 && (
          <>
            <h6>Requirements</h6>
            <ul>
              {job.requirements.map((r, i) => <li key={i}>{r}</li>)}
            </ul>
          </>
        )}

        {user && user.role === 'candidate' && (
          <form onSubmit={handleApply} data-testid="apply-form">
            <label className="form-label mt-2">Cover letter (optional)</label>
            <textarea
              className="form-control mb-2"
              rows={3}
              value={coverLetter}
              onChange={(e) => setCoverLetter(e.target.value)}
              data-testid="input-cover-letter"
              maxLength={3000}
            />
            {error && <div className="alert alert-danger py-2" data-testid="apply-error">{error}</div>}
            <button type="submit" className="btn btn-ch-primary" disabled={submitting} data-testid="btn-submit-application">
              {submitting ? 'Submitting...' : 'Apply now'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

const backdropStyle = {
  position: 'fixed',
  inset: 0,
  background: 'rgba(15,23,42,0.5)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  zIndex: 1050,
  padding: '1rem'
};

const modalStyle = {
  background: '#fff',
  borderRadius: 16,
  padding: '1.75rem',
  maxWidth: 640,
  width: '100%',
  maxHeight: '85vh',
  overflowY: 'auto'
};
