const express = require('express');
const mongoose = require('mongoose');
const Job = require('../models/Job');
const { requireAuth, requireRole } = require('../middleware/auth');

const router = express.Router();

// GET /api/jobs?search=&company=&skills=&type=&experience=&page=&limit=
router.get('/', async (req, res) => {
  try {
    const { search, company, skills, type, experience } = req.query;
    const page = Math.max(parseInt(req.query.page, 10) || 1, 1);
    const limit = Math.min(Math.max(parseInt(req.query.limit, 10) || 10, 1), 50);

    const filter = { isActive: true };

    if (search && String(search).trim()) {
      const re = new RegExp(String(search).trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i');
      filter.$or = [{ title: re }, { company: re }, { skills: re }];
    }
    if (company && String(company).trim()) {
      filter.company = new RegExp(String(company).trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i');
    }
    if (skills && String(skills).trim()) {
      const list = String(skills).split(',').map((s) => s.trim()).filter(Boolean);
      if (list.length) filter.skills = { $in: list };
    }
    if (type && String(type).trim()) {
      filter.employmentType = type;
    }
    if (experience && String(experience).trim()) {
      filter.experienceLevel = experience;
    }

    const total = await Job.countDocuments(filter);
    const jobs = await Job.find(filter)
      .sort({ createdAt: -1 })
      .skip((page - 1) * limit)
      .limit(limit);

    return res.json({
      jobs,
      pagination: { page, limit, total, totalPages: Math.max(Math.ceil(total / limit), 1) }
    });
  } catch (err) {
    return res.status(500).json({ message: 'Failed to fetch jobs', error: err.message });
  }
});

router.get('/:id', async (req, res) => {
  try {
    if (!mongoose.isValidObjectId(req.params.id)) {
      return res.status(400).json({ message: 'Invalid job id' });
    }
    const job = await Job.findById(req.params.id);
    if (!job) return res.status(404).json({ message: 'Job not found' });
    return res.json({ job });
  } catch (err) {
    return res.status(500).json({ message: 'Failed to fetch job', error: err.message });
  }
});

router.post('/', requireAuth, requireRole('recruiter'), async (req, res) => {
  try {
    const {
      title, company, location, employmentType, experienceLevel,
      skills, description, requirements, salaryMin, salaryMax
    } = req.body || {};

    if (!title || String(title).trim().length < 2 || String(title).trim().length > 120) {
      return res.status(400).json({ message: 'Title must be between 2 and 120 characters' });
    }
    if (!company || String(company).trim().length < 2) {
      return res.status(400).json({ message: 'Company is required' });
    }
    if (!description || String(description).trim().length < 10) {
      return res.status(400).json({ message: 'Description must be at least 10 characters' });
    }
    if (salaryMin != null && salaryMax != null && Number(salaryMin) > Number(salaryMax)) {
      return res.status(400).json({ message: 'salaryMin cannot exceed salaryMax' });
    }

    const job = await Job.create({
      title: String(title).trim(),
      company: String(company).trim(),
      location: location || 'Remote',
      employmentType: employmentType || 'Full-time',
      experienceLevel: experienceLevel || 'Fresher',
      skills: Array.isArray(skills) ? skills : [],
      description,
      requirements: Array.isArray(requirements) ? requirements : [],
      salaryMin: Number(salaryMin) || 0,
      salaryMax: Number(salaryMax) || 0,
      postedBy: req.user.sub
    });

    return res.status(201).json({ job });
  } catch (err) {
    return res.status(500).json({ message: 'Failed to create job', error: err.message });
  }
});

router.put('/:id', requireAuth, requireRole('recruiter'), async (req, res) => {
  try {
    if (!mongoose.isValidObjectId(req.params.id)) {
      return res.status(400).json({ message: 'Invalid job id' });
    }
    const job = await Job.findById(req.params.id);
    if (!job) return res.status(404).json({ message: 'Job not found' });
    if (job.postedBy.toString() !== req.user.sub) {
      return res.status(403).json({ message: 'You can only edit jobs you posted' });
    }

    const allowed = [
      'title', 'company', 'location', 'employmentType', 'experienceLevel',
      'skills', 'description', 'requirements', 'salaryMin', 'salaryMax', 'isActive'
    ];
    for (const key of allowed) {
      if (req.body[key] !== undefined) job[key] = req.body[key];
    }
    await job.save();
    return res.json({ job });
  } catch (err) {
    return res.status(500).json({ message: 'Failed to update job', error: err.message });
  }
});

router.delete('/:id', requireAuth, requireRole('recruiter'), async (req, res) => {
  try {
    if (!mongoose.isValidObjectId(req.params.id)) {
      return res.status(400).json({ message: 'Invalid job id' });
    }
    const job = await Job.findById(req.params.id);
    if (!job) return res.status(404).json({ message: 'Job not found' });
    if (job.postedBy.toString() !== req.user.sub) {
      return res.status(403).json({ message: 'You can only delete jobs you posted' });
    }
    await job.deleteOne();
    return res.json({ message: 'Job deleted' });
  } catch (err) {
    return res.status(500).json({ message: 'Failed to delete job', error: err.message });
  }
});

router.get('/recruiter/mine', requireAuth, requireRole('recruiter'), async (req, res) => {
  try {
    const jobs = await Job.find({ postedBy: req.user.sub }).sort({ createdAt: -1 });
    return res.json({ jobs });
  } catch (err) {
    return res.status(500).json({ message: 'Failed to fetch jobs', error: err.message });
  }
});

module.exports = router;
