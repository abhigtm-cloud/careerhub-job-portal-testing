const express = require('express');
const mongoose = require('mongoose');
const SavedJob = require('../models/SavedJob');
const Job = require('../models/Job');
const { requireAuth, requireRole } = require('../middleware/auth');

const router = express.Router();

router.get('/', requireAuth, requireRole('candidate'), async (req, res) => {
  try {
    const saved = await SavedJob.find({ candidate: req.user.sub })
      .sort({ createdAt: -1 })
      .populate('job');
    return res.json({ savedJobs: saved });
  } catch (err) {
    return res.status(500).json({ message: 'Failed to fetch saved jobs', error: err.message });
  }
});

router.post('/', requireAuth, requireRole('candidate'), async (req, res) => {
  try {
    const { jobId } = req.body || {};
    if (!mongoose.isValidObjectId(jobId)) {
      return res.status(400).json({ message: 'Invalid job id' });
    }
    const job = await Job.findById(jobId);
    if (!job) return res.status(404).json({ message: 'Job not found' });

    const existing = await SavedJob.findOne({ job: jobId, candidate: req.user.sub });
    if (existing) return res.status(409).json({ message: 'Job already saved' });

    const saved = await SavedJob.create({ job: jobId, candidate: req.user.sub });
    return res.status(201).json({ savedJob: saved });
  } catch (err) {
    if (err && err.code === 11000) {
      return res.status(409).json({ message: 'Job already saved' });
    }
    return res.status(500).json({ message: 'Failed to save job', error: err.message });
  }
});

router.delete('/:jobId', requireAuth, requireRole('candidate'), async (req, res) => {
  try {
    if (!mongoose.isValidObjectId(req.params.jobId)) {
      return res.status(400).json({ message: 'Invalid job id' });
    }
    const result = await SavedJob.findOneAndDelete({ job: req.params.jobId, candidate: req.user.sub });
    if (!result) return res.status(404).json({ message: 'Saved job not found' });
    return res.json({ message: 'Removed from saved jobs' });
  } catch (err) {
    return res.status(500).json({ message: 'Failed to remove saved job', error: err.message });
  }
});

module.exports = router;
