import { SearchX } from 'lucide-react';

export default function EmptyState({ title = 'Nothing here yet', subtitle = '', action = null }) {
  return (
    <div className="empty-state" data-testid="empty-state">
      <SearchX size={40} className="mb-3 text-muted" />
      <h5>{title}</h5>
      {subtitle && <p className="mb-3">{subtitle}</p>}
      {action}
    </div>
  );
}
