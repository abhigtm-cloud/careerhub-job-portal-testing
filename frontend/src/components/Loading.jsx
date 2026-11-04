export default function Loading({ label = 'Loading...' }) {
  return (
    <div className="d-flex align-items-center justify-content-center py-5" data-testid="loading-state">
      <div className="spinner-border text-primary me-2" role="status" aria-hidden="true"></div>
      <span>{label}</span>
    </div>
  );
}
