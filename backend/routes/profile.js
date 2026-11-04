const express = require('express');
const User = require('../models/User');
const { requireAuth } = require('../middleware/auth');

const router = express.Router();

function sanitizeUser(user) {
  return {
    id: user._id,
    name: user.name,
    email: user.email,
    role: user.role,
    headline: user.headline,
    phone: user.phone,
    skills: user.skills,
    company: user.company
  };
}

router.get('/', requireAuth, async (req, res) => {
  const user = await User.findById(req.user.sub);
  if (!user) return res.status(404).json({ message: 'User not found' });
  return res.json({ user: sanitizeUser(user) });
});

router.put('/', requireAuth, async (req, res) => {
  try {
    const user = await User.findById(req.user.sub);
    if (!user) return res.status(404).json({ message: 'User not found' });

    const { name, headline, phone, skills, company } = req.body || {};

    if (name !== undefined) {
      if (String(name).trim().length < 2 || String(name).trim().length > 80) {
        return res.status(400).json({ message: 'Name must be between 2 and 80 characters' });
      }
      user.name = String(name).trim();
    }
    if (headline !== undefined) {
      if (String(headline).length > 120) {
        return res.status(400).json({ message: 'Headline must be at most 120 characters' });
      }
      user.headline = String(headline);
    }
    if (phone !== undefined) {
      if (phone && !/^[0-9+\-\s()]{7,20}$/.test(String(phone))) {
        return res.status(400).json({ message: 'Invalid phone number format' });
      }
      user.phone = String(phone);
    }
    if (skills !== undefined) {
      if (!Array.isArray(skills)) {
        return res.status(400).json({ message: 'Skills must be an array' });
      }
      user.skills = skills.map((s) => String(s).trim()).filter(Boolean).slice(0, 30);
    }
    if (company !== undefined) {
      user.company = String(company).slice(0, 100);
    }

    await user.save();
    return res.json({ user: sanitizeUser(user) });
  } catch (err) {
    return res.status(500).json({ message: 'Failed to update profile', error: err.message });
  }
});

module.exports = router;
