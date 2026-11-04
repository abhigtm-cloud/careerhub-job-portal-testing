import { useEffect, useState } from 'react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext.jsx';
import Loading from '../components/Loading.jsx';
import EmptyState from '../components/EmptyState.jsx';

const EMPTY_JOB = {
  title: '', company: '', location: 'Remote', employmentType: 'Full-time',
  experienceLevel: 'Fresher', skills: '', description: '', requirements: '',
  salaryMin: '', salaryMax: ''
};

function StatsPanel() {
  const [stats, setStats] = useState(null);
  useEffect(() => { api.get('/recruiter/stats').then(setStats).catch(() => {}); }, []);
  if (!stats) return <Loading label="Loading stats..." />;
  return (
    <div className="row g-3" data-testid="stats-panel">
      <div className="col-6 col-md-3">
        <div className="stat-card"><div className="stat-value" data-testid="stat-total-jobs">{stats.totalJobs}</div><div>Total jobs</div></div>
      </div>
      <div className="col-6 col-md-3">
        <div className="stat-card"><div className="stat-value" data-testid="stat-active-jobs">{stats.activeJobs}</div><div>Active jobs</div></div>
      </div>
      <div className="col-6 col-md-3">
        <div className="stat-card"><div className="stat-value" data-testid="stat-total-applications">{stats.totalApplications}</div><div>Applications</div></div>
      </div>
      <div className="col-6 col-md-3">
        <div className="stat-card"><div className="stat-value">{stats.statusCounts?.hired || 0}</div><div>Hired</div></div>
      </div>
    </div>
  );
}

function PostJobForm({ onCreated }) {
  const { showToast } = useToast();
  const [form, setForm] = useState(EMPTY_JOB);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  function update(field, value) { setForm((prev) => ({ ...prev, [field]: value })); }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    if (form.title.trim().length < 2) return setError('Title is required');
    if (form.company.trim().length < 2) return setError('Company is required');
    if (form.description.trim().length < 10) return setError('Description must be at least 10 characters');
    if (form.salaryMin && form.salaryMax && Number(form.salaryMin) > Number(form.salaryMax)) {
      return setError('Minimum salary cannot exceed maximum salary');
    }

    setSubmitting(true);
    try {
      const payload = {
        ...form,
        skills: form.skills.split(',').map((s) => s.trim()).filter(Boolean),
        requirements: form.requirements.split('\n').map((s) => s.trim()).filter(Boolean),
        salaryMin: Number(form.salaryMin) || 0,
        salaryMax: Number(form.salaryMax) || 0
      };
      await api.post('/jobs', payload);
      showToast('Job posted successfully', 'success');
      setForm(EMPTY_JOB);
      onCreated && onCreated();
    } catch (err) {
      setError(err.message || 'Failed to post job');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} data-testid="post-job-form" className="dashboard-card">
      <div className="row">
        <div className="col-md-6 mb-3">
          <label className="form-label">Job title</label>
          <input className="form-control" value={form.title} onChange={(e) => update('title', e.target.value)} data-testid="input-job-title" />
        </div>
        <div className="col-md-6 mb-3">
          <label className="form-label">Company</label>
          <input className="form-control" value={form.company} onChange={(e) => update('company', e.target.value)} data-testid="input-job-company" />
        </div>
        <div className="col-md-4 mb-3">
          <label className="form-label">Location</label>
          <input className="form-control" value={form.location} onChange={(e) => update('location', e.target.value)} data-testid="input-job-location" />
        </div>
        <div className="col-md-4 mb-3">
          <label className="form-label">Employment type</label>
          <select className="form-select" value={form.employmentType} onChange={(e) => update('employmentType', e.target.value)} data-testid="select-job-type">
            {['Full-time', 'Part-time', 'Internship', 'Contract'].map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>
        <div className="col-md-4 mb-3">
          <label className="form-label">Experience level</label>
          <select className="form-select" value={form.experienceLevel} onChange={(e) => update('experienceLevel', e.target.value)} data-testid="select-job-experience">
            {['Fresher', 'Junior', 'Mid', 'Senior', 'Lead'].map((l) => <option key={l} value={l}>{l}</option>)}
          </select>
        </div>
        <div className="col-md-6 mb-3">
          <label className="form-label">Skills (comma separated)</label>
          <input className="form-control" value={form.skills} onChange={(e) => update('skills', e.target.value)} data-testid="input-job-skills" />
        </div>
        <div className="col-md-3 mb-3">
          <label className="form-label">Min salary</label>
          <input type="number" min="0" className="form-control" value={form.salaryMin} onChange={(e) => update('salaryMin', e.target.value)} data-testid="input-job-salary-min" />
        </div>
        <div className="col-md-3 mb-3">
          <label className="form-label">Max salary</label>
          <input type="number" min="0" className="form-control" value={form.salaryMax} onChange={(e) => update('salaryMax', e.target.value)} data-testid="input-job-salary-max" />
        </div>
        <div className="col-12 mb-3">
          <label className="form-label">Description</label>
          <textarea className="form-control" rows={3} value={form.description} onChange={(e) => update('description', e.target.value)} data-testid="input-job-description" />
        </div>
        <div className="col-12 mb-3">
          <label className="form-label">Requirements (one per line)</label>
          <textarea className="form-control" rows={3} value={form.requirements} onChange={(e) => update('requirements', e.target.value)} data-testid="input-job-requirements" />
        </div>
      </div>
      {error && <div className="alert alert-danger py-2" data-testid="post-job-error">{error}</div>}
      <button type="submit" className="btn btn-ch-primary" disabled={submitting} data-testid="btn-post-job">
        {submitting ? 'Posting...' : 'Post job'}
      </button>
    </form>
  );
}

function MyJobsList({ jobs, onEdit, onDeleted, onViewApplications }) {
  const { showToast } = useToast();

  async function handleDelete(job) {
    if (!window.confirm(`Delete "${job.title}"? This cannot be undone.`)) return;
    try {
      await api.del(`/jobs/${job._id}`);
      showToast('Job deleted', 'success');
      onDeleted();
    } catch (err) {
      showToast(err.message || 'Failed to delete job', 'error');
    }
  }

  if (jobs.length === 0) {
    return <EmptyState title="You haven't posted any jobs yet" subtitle="Use the Post Job tab to create your first listing." />;
  }

  return (
    <div data-testid="recruiter-jobs-list">
      {jobs.map((job) => (
        <div key={job._id} className="dashboard-card mb-3" data-testid="recruiter-job-item">
          <div className="d-flex justify-content-between align-items-start flex-wrap gap-2">
            <div>
              <h5>{job.title}</h5>
              <div className="text-muted small">{job.company} &middot; {job.location} &middot; {job.employmentType}</div>
            </div>
            <div className="d-flex gap-2">
              <button className="btn btn-sm btn-outline-primary" onClick={() => onViewApplications(job)} data-testid="btn-view-applications">
                Applications
              </button>
              <button className="btn btn-sm btn-outline-secondary" onClick={() => onEdit(job)} data-testid="btn-edit-job">
                Edit
              </button>
              <button className="btn btn-sm btn-outline-danger" onClick={() => handleDelete(job)} data-testid="btn-delete-job">
                Delete
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

function EditJobModal({ job, onClose, onSaved }) {
  const { showToast } = useToast();
  const [form, setForm] = useState({
    ...job,
    skills: (job.skills || []).join(', '),
    requirements: (job.requirements || []).join('\n')
  });
  const [error, setError] = useState('');

  function update(field, value) { setForm((prev) => ({ ...prev, [field]: value })); }

  async function handleSave(e) {
    e.preventDefault();
    setError('');
    try {
      await api.put(`/jobs/${job._id}`, {
        ...form,
        skills: form.skills.split(',').map((s) => s.trim()).filter(Boolean),
        requirements: form.requirements.split('\n').map((s) => s.trim()).filter(Boolean),
        salaryMin: Number(form.salaryMin) || 0,
        salaryMax: Number(form.salaryMax) || 0
      });
      showToast('Job updated', 'success');
      onSaved();
    } catch (err) {
      setError(err.message || 'Failed to update job');
    }
  }

  return (
    <div style={{ position: 'fixed', inset: 0, background: 'rgba(15,23,42,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1050, padding: '1rem' }} data-testid="edit-job-modal">
      <div style={{ background: '#fff', borderRadius: 16, padding: '1.5rem', maxWidth: 560, width: '100%', maxHeight: '85vh', overflowY: 'auto' }}>
        <h5 className="mb-3">Edit job</h5>
        <form onSubmit={handleSave}>
          <label className="form-label">Title</label>
          <input className="form-control mb-2" value={form.title} onChange={(e) => update('title', e.target.value)} data-testid="edit-input-title" />
          <label className="form-label">Description</label>
          <textarea className="form-control mb-2" rows={3} value={form.description} onChange={(e) => update('description', e.target.value)} data-testid="edit-input-description" />
          <label className="form-label">Active</label>
          <select className="form-select mb-3" value={String(form.isActive)} onChange={(e) => update('isActive', e.target.value === 'true')} data-testid="edit-select-active">
            <option value="true">Active</option>
            <option value="false">Inactive</option>
          </select>
          {error && <div className="alert alert-danger py-2">{error}</div>}
          <div className="d-flex gap-2">
            <button type="submit" className="btn btn-ch-primary" data-testid="btn-save-edit-job">Save changes</button>
            <button type="button" className="btn btn-outline-secondary" onClick={onClose} data-testid="btn-cancel-edit-job">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}

function ApplicationsModal({ job, onClose }) {
  const [applications, setApplications] = useState(null);

  useEffect(() => {
    api.get(`/applications/job/${job._id}`).then((data) => setApplications(data.applications));
  }, [job._id]);

  return (
    <div style={{ position: 'fixed', inset: 0, background: 'rgba(15,23,42,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1050, padding: '1rem' }} data-testid="applications-modal">
      <div style={{ background: '#fff', borderRadius: 16, padding: '1.5rem', maxWidth: 640, width: '100%', maxHeight: '85vh', overflowY: 'auto' }}>
        <div className="d-flex justify-content-between mb-3">
          <h5>Applications for {job.title}</h5>
          <button className="btn btn-sm btn-light" onClick={onClose} data-testid="btn-close-applications-modal">Close</button>
        </div>
        {applications === null ? (
          <Loading label="Loading applications..." />
        ) : applications.length === 0 ? (
          <EmptyState title="No applications yet" />
        ) : (
          <div data-testid="job-applications-list">
            {applications.map((app) => (
              <div key={app._id} className="dashboard-card mb-2" data-testid="job-application-item">
                <strong>{app.candidate?.name}</strong> &middot; {app.candidate?.email}
                <div className="text-muted small">{(app.candidate?.skills || []).join(', ')}</div>
                {app.coverLetter && <p className="mb-0 mt-1 small">{app.coverLetter}</p>}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default function RecruiterDashboardPage() {
  const [tab, setTab] = useState('overview');
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingJob, setEditingJob] = useState(null);
  const [applicationsJob, setApplicationsJob] = useState(null);

  function loadJobs() {
    setLoading(true);
    api.get('/jobs/recruiter/mine').then((data) => setJobs(data.jobs)).finally(() => setLoading(false));
  }

  useEffect(() => { loadJobs(); }, []);

  const tabs = [
    { key: 'overview', label: 'Overview' },
    { key: 'jobs', label: 'My Jobs' },
    { key: 'post', label: 'Post Job' }
  ];

  return (
    <div className="container py-4">
      <h3 className="mb-4">Recruiter Dashboard</h3>
      <ul className="nav nav-pills mb-4" data-testid="recruiter-tabs">
        {tabs.map((t) => (
          <li className="nav-item" key={t.key}>
            <button
              className={`nav-link ${tab === t.key ? 'active' : ''}`}
              onClick={() => setTab(t.key)}
              data-testid={`tab-${t.key}`}
            >
              {t.label}
            </button>
          </li>
        ))}
      </ul>

      {tab === 'overview' && <StatsPanel />}
      {tab === 'post' && <PostJobForm onCreated={() => { loadJobs(); setTab('jobs'); }} />}
      {tab === 'jobs' && (
        loading ? <Loading label="Loading your jobs..." /> : (
          <MyJobsList
            jobs={jobs}
            onEdit={setEditingJob}
            onDeleted={loadJobs}
            onViewApplications={setApplicationsJob}
          />
        )
      )}

      {editingJob && (
        <EditJobModal
          job={editingJob}
          onClose={() => setEditingJob(null)}
          onSaved={() => { setEditingJob(null); loadJobs(); }}
        />
      )}
      {applicationsJob && (
        <ApplicationsModal job={applicationsJob} onClose={() => setApplicationsJob(null)} />
      )}
    </div>
  );
}
