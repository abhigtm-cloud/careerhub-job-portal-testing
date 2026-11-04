import { useCallback, useEffect, useState } from 'react';
import { Search } from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext.jsx';
import { useToast } from '../context/ToastContext.jsx';
import JobCard from '../components/JobCard.jsx';
import JobDetailModal from '../components/JobDetailModal.jsx';
import Loading from '../components/Loading.jsx';
import EmptyState from '../components/EmptyState.jsx';

const EMPLOYMENT_TYPES = ['Full-time', 'Part-time', 'Internship', 'Contract'];
const EXPERIENCE_LEVELS = ['Fresher', 'Junior', 'Mid', 'Senior', 'Lead'];

export default function JobsPage() {
  const { user } = useAuth();
  const { showToast } = useToast();

  const [search, setSearch] = useState('');
  const [company, setCompany] = useState('');
  const [type, setType] = useState('');
  const [experience, setExperience] = useState('');
  const [page, setPage] = useState(1);

  const [jobs, setJobs] = useState([]);
  const [pagination, setPagination] = useState({ page: 1, totalPages: 1 });
  const [loading, setLoading] = useState(true);
  const [activeJob, setActiveJob] = useState(null);
  const [savedIds, setSavedIds] = useState(new Set());

  const fetchJobs = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (search.trim()) params.set('search', search.trim());
      if (company.trim()) params.set('company', company.trim());
      if (type) params.set('type', type);
      if (experience) params.set('experience', experience);
      params.set('page', String(page));
      params.set('limit', '6');

      const data = await api.get(`/jobs?${params.toString()}`);
      setJobs(data.jobs);
      setPagination(data.pagination);
    } catch (err) {
      showToast(err.message || 'Failed to load jobs', 'error');
    } finally {
      setLoading(false);
    }
  }, [search, company, type, experience, page, showToast]);

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  useEffect(() => {
    if (user && user.role === 'candidate') {
      api.get('/saved-jobs').then((data) => {
        setSavedIds(new Set(data.savedJobs.map((s) => s.job?._id)));
      }).catch(() => {});
    }
  }, [user]);

  function handleSearchSubmit(e) {
    e.preventDefault();
    setPage(1);
    fetchJobs();
  }

  function resetFilters() {
    setSearch('');
    setCompany('');
    setType('');
    setExperience('');
    setPage(1);
  }

  async function toggleSave(job) {
    if (!user) {
      showToast('Please log in as a candidate to save jobs', 'error');
      return;
    }
    try {
      if (savedIds.has(job._id)) {
        await api.del(`/saved-jobs/${job._id}`);
        setSavedIds((prev) => {
          const next = new Set(prev);
          next.delete(job._id);
          return next;
        });
        showToast('Removed from saved jobs', 'success');
      } else {
        await api.post('/saved-jobs', { jobId: job._id });
        setSavedIds((prev) => new Set(prev).add(job._id));
        showToast('Job saved', 'success');
      }
    } catch (err) {
      showToast(err.message || 'Action failed', 'error');
    }
  }

  return (
    <>
      <div className="hero">
        <div className="container">
          <h1 data-testid="hero-title">Find your next opportunity</h1>
          <p className="mb-4">Search thousands of roles from companies that are hiring right now.</p>
          <form className="search-bar d-flex gap-2 flex-wrap" onSubmit={handleSearchSubmit} data-testid="search-form">
            <input
              type="text"
              className="form-control flex-grow-1"
              placeholder="Job title, company or skill"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              data-testid="input-search"
              maxLength={120}
            />
            <button type="submit" className="btn btn-ch-primary" data-testid="btn-search">
              <Search size={16} className="me-1" /> Search
            </button>
          </form>
        </div>
      </div>

      <div className="container py-4">
        <div className="row">
          <div className="col-lg-3 mb-4">
            <div className="sidebar-filters" data-testid="filters-sidebar">
              <h6 className="mb-3">Filters</h6>
              <label className="form-label small">Company</label>
              <input
                className="form-control form-control-sm mb-3"
                value={company}
                onChange={(e) => { setCompany(e.target.value); setPage(1); }}
                data-testid="input-filter-company"
              />
              <label className="form-label small">Employment type</label>
              <select
                className="form-select form-select-sm mb-3"
                value={type}
                onChange={(e) => { setType(e.target.value); setPage(1); }}
                data-testid="select-filter-type"
              >
                <option value="">All types</option>
                {EMPLOYMENT_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
              </select>
              <label className="form-label small">Experience</label>
              <select
                className="form-select form-select-sm mb-3"
                value={experience}
                onChange={(e) => { setExperience(e.target.value); setPage(1); }}
                data-testid="select-filter-experience"
              >
                <option value="">All levels</option>
                {EXPERIENCE_LEVELS.map((l) => <option key={l} value={l}>{l}</option>)}
              </select>
              <button className="btn btn-outline-secondary btn-sm w-100" onClick={resetFilters} data-testid="btn-reset-filters">
                Reset filters
              </button>
            </div>
          </div>

          <div className="col-lg-9">
            {loading ? (
              <Loading label="Loading jobs..." />
            ) : jobs.length === 0 ? (
              <EmptyState
                title="No jobs match your search"
                subtitle="Try adjusting your filters or search terms."
                action={<button className="btn btn-ch-primary" onClick={resetFilters}>Reset filters</button>}
              />
            ) : (
              <>
                <div data-testid="job-list">
                  {jobs.map((job) => (
                    <JobCard
                      key={job._id}
                      job={job}
                      onOpen={setActiveJob}
                      onToggleSave={toggleSave}
                      isSaved={savedIds.has(job._id)}
                      showSaveButton={!!user && user.role === 'candidate'}
                    />
                  ))}
                </div>
                {pagination.totalPages > 1 && (
                  <nav data-testid="pagination">
                    <ul className="pagination">
                      {Array.from({ length: pagination.totalPages }, (_, i) => i + 1).map((p) => (
                        <li key={p} className={`page-item ${p === page ? 'active' : ''}`}>
                          <button className="page-link" onClick={() => setPage(p)} data-testid={`page-${p}`}>
                            {p}
                          </button>
                        </li>
                      ))}
                    </ul>
                  </nav>
                )}
              </>
            )}
          </div>
        </div>
      </div>

      {activeJob && (
        <JobDetailModal job={activeJob} onClose={() => setActiveJob(null)} />
      )}
    </>
  );
}
