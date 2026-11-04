import { MapPin, Briefcase, Bookmark, BookmarkCheck } from 'lucide-react';

function formatSalary(min, max) {
  if (!min && !max) return 'Not disclosed';
  const fmt = (n) => (n >= 100000 ? `${(n / 100000).toFixed(1)}L` : n.toLocaleString());
  return `₹${fmt(min)} - ₹${fmt(max)}`;
}

export default function JobCard({ job, onOpen, onToggleSave, isSaved, showSaveButton }) {
  return (
    <div className="job-card p-4 mb-3" data-testid="job-card" data-job-id={job._id}>
      <div className="d-flex justify-content-between align-items-start">
        <div>
          <h5 className="mb-1" data-testid="job-title">{job.title}</h5>
          <div className="text-muted mb-2">{job.company}</div>
        </div>
        {showSaveButton && (
          <button
            className="btn btn-sm btn-outline-secondary"
            onClick={() => onToggleSave(job)}
            data-testid="btn-toggle-save"
            aria-label="Save job"
          >
            {isSaved ? <BookmarkCheck size={16} /> : <Bookmark size={16} />}
          </button>
        )}
      </div>
      <div className="d-flex gap-3 text-muted small mb-2">
        <span><MapPin size={14} className="me-1" />{job.location}</span>
        <span><Briefcase size={14} className="me-1" />{job.employmentType}</span>
        <span>{job.experienceLevel}</span>
      </div>
      <div className="mb-2">
        {(job.skills || []).slice(0, 5).map((s) => (
          <span key={s} className="badge-skill">{s}</span>
        ))}
      </div>
      <div className="d-flex justify-content-between align-items-center">
        <span className="fw-semibold">{formatSalary(job.salaryMin, job.salaryMax)}</span>
        <button className="btn btn-ch-primary btn-sm" onClick={() => onOpen(job)} data-testid="btn-view-job">
          View details
        </button>
      </div>
    </div>
  );
}
