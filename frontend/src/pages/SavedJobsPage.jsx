import { useEffect, useState } from 'react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext.jsx';
import JobCard from '../components/JobCard.jsx';
import JobDetailModal from '../components/JobDetailModal.jsx';
import Loading from '../components/Loading.jsx';
import EmptyState from '../components/EmptyState.jsx';

export default function SavedJobsPage() {
  const { showToast } = useToast();
  const [saved, setSaved] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeJob, setActiveJob] = useState(null);

  function load() {
    setLoading(true);
    api.get('/saved-jobs')
      .then((data) => setSaved(data.savedJobs.filter((s) => s.job)))
      .finally(() => setLoading(false));
  }

  useEffect(() => { load(); }, []);

  async function removeSaved(job) {
    try {
      await api.del(`/saved-jobs/${job._id}`);
      setSaved((prev) => prev.filter((s) => s.job._id !== job._id));
      showToast('Removed from saved jobs', 'success');
    } catch (err) {
      showToast(err.message || 'Failed to remove job', 'error');
    }
  }

  if (loading) return <Loading label="Loading saved jobs..." />;

  return (
    <div className="container py-4">
      <h3 className="mb-4">Saved Jobs</h3>
      {saved.length === 0 ? (
        <EmptyState title="No saved jobs" subtitle="Save jobs you're interested in to find them here later." />
      ) : (
        <div data-testid="saved-jobs-list">
          {saved.map((s) => (
            <JobCard
              key={s._id}
              job={s.job}
              onOpen={setActiveJob}
              onToggleSave={removeSaved}
              isSaved={true}
              showSaveButton={true}
            />
          ))}
        </div>
      )}
      {activeJob && <JobDetailModal job={activeJob} onClose={() => setActiveJob(null)} />}
    </div>
  );
}
