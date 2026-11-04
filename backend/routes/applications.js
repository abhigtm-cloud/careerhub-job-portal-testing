const express = require('express');
const mongoose = require('mongoose');
const Application = require('../models/Application');
const Job = require('../models/Job');
const { requireAuth, requireRole } = require('../middleware/auth');

const router = express.Router();

router.post('/', requireAuth, requireRole('candidate'), async (req, res) => {
  try {
    const { jobId, coverLetter } = req.body || {};
    if (!mongoose.isValidObjectId(jobId)) {
      return res.status(400).json({ message: 'Invalid job id' });
    }
    const job = await Job.findById(jobId);
    if (!job) return res.status(404).json({ message: 'Job not found' });

    const existing = await Application.findOne({ job: jobId, candidate: req.user.sub });
    if (existing) {
      return res.status(409).json({ message: 'You have already applied to this job' });
    }

    const application = await Application.create({
      job: jobId,
      candidate: req.user.sub,
      coverLetter: typeof coverLetter === 'string' ? coverLetter.slice(0, 3000) : ''
    });

    return res.status(201).json({ application });
  } catch (err) {
    if (err && err.code === 11000) {
      return res.status(409).json({ message: 'You have already applied to this job' });
    }
    return res.status(500).json({ message: 'Failed to submit application', error: err.message });
  }
});

router.get('/mine', requireAuth, requireRole('candidate'), async (req, res) => {
  try {
    const applications = await Application.find({ candidate: req.user.sub })
      .sort({ createdAt: -1 })
      .populate('job');
    return res.json({ applications });
  } catch (err) {
    return res.status(500).json({ message: 'Failed to fetch applications', error: err.message });
  }
});

router.get('/job/:jobId', requireAuth, requireRole('recruiter'), async (req, res) => {
  try {
    if (!mongoose.isValidObjectId(req.params.jobId)) {
      return res.status(400).json({ message: 'Invalid job id' });
    }
    const job = await Job.findById(req.params.jobId);
    if (!job) return res.status(404).json({ message: 'Job not found' });
    if (job.postedBy.toString() !== req.user.sub) {
      return res.status(403).json({ message: 'You can only view applications for your own jobs' });
    }
    const applications = await Application.find({ job: req.params.jobId })
      .sort({ createdAt: -1 })
      .populate('candidate', 'name email headline skills phone');
    return res.json({ applications });
  } catch (err) {
    return res.status(500).json({ message: 'Failed to fetch applications', error: err.message });
  }
});

module.exports = router;
