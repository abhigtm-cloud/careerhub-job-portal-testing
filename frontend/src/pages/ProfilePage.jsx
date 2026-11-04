import { useState } from 'react';
import { X } from 'lucide-react';
import { useAuth } from '../context/AuthContext.jsx';
import { useToast } from '../context/ToastContext.jsx';
import { api } from '../api/client';

export default function ProfilePage() {
  const { user, updateUser } = useAuth();
  const { showToast } = useToast();

  const [name, setName] = useState(user.name);
  const [headline, setHeadline] = useState(user.headline || '');
  const [phone, setPhone] = useState(user.phone || '');
  const [skills, setSkills] = useState(user.skills || []);
  const [skillInput, setSkillInput] = useState('');
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  function addSkill() {
    const value = skillInput.trim();
    if (!value) return;
    if (skills.includes(value)) { setSkillInput(''); return; }
    setSkills((prev) => [...prev, value]);
    setSkillInput('');
  }

  function removeSkill(skill) {
    setSkills((prev) => prev.filter((s) => s !== skill));
  }

  async function handleSave(e) {
    e.preventDefault();
    setError('');
    setSaving(true);
    try {
      const data = await api.put('/profile', { name, headline, phone, skills });
      updateUser(data.user);
      showToast('Profile updated', 'success');
    } catch (err) {
      setError(err.message || 'Failed to save profile');
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="container py-4">
      <h3 className="mb-4">My Profile</h3>
      <div className="dashboard-card" style={{ maxWidth: 560 }}>
        <form onSubmit={handleSave} data-testid="profile-form">
          <label className="form-label">Full name</label>
          <input className="form-control mb-3" value={name} onChange={(e) => setName(e.target.value)} data-testid="input-profile-name" />

          <label className="form-label">Headline</label>
          <input className="form-control mb-3" value={headline} onChange={(e) => setHeadline(e.target.value)} data-testid="input-profile-headline" maxLength={120} />

          <label className="form-label">Phone number</label>
          <input className="form-control mb-3" value={phone} onChange={(e) => setPhone(e.target.value)} data-testid="input-profile-phone" />

          <label className="form-label">Skills</label>
          <div className="mb-2" data-testid="skills-list">
            {skills.map((s) => (
              <span key={s} className="skill-chip" data-testid="skill-chip">
                {s}
                <button type="button" onClick={() => removeSkill(s)} data-testid="btn-remove-skill" aria-label={`Remove ${s}`}>
                  <X size={12} />
                </button>
              </span>
            ))}
          </div>
          <div className="d-flex gap-2 mb-3">
            <input
              className="form-control"
              value={skillInput}
              onChange={(e) => setSkillInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addSkill(); } }}
              placeholder="Add a skill and press Enter"
              data-testid="input-add-skill"
            />
            <button type="button" className="btn btn-outline-secondary" onClick={addSkill} data-testid="btn-add-skill">
              Add
            </button>
          </div>

          {error && <div className="alert alert-danger py-2" data-testid="profile-error">{error}</div>}

          <button type="submit" className="btn btn-ch-primary" disabled={saving} data-testid="btn-save-profile">
            {saving ? 'Saving...' : 'Save changes'}
          </button>
        </form>
      </div>
    </div>
  );
}
