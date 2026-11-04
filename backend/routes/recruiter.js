const express = require('express');
const Job = require('../models/Job');
const Application = require('../models/Application');
const { requireAuth, requireRole } = require('../middleware/auth');

const router = express.Router();

router.get('/stats', requireAuth, requireRole('recruiter'), async (req, res) => {
  try {
    const jobs = await Job.find({ postedBy: req.user.sub });
    const jobIds = jobs.map((j) => j._id);
    const totalApplications = await Application.countDocuments({ job: { $in: jobIds } });
    const byStatus = await Application.aggregate([
      { $match: { job: { $in: jobIds } } },
      { $group: { _id: '$status', count: { $sum: 1 } } }
    ]);

    const statusCounts = byStatus.reduce((acc, row) => {
      acc[row._id] = row.count;
      return acc;
    }, {});

    return res.json({
      totalJobs: jobs.length,
      activeJobs: jobs.filter((j) => j.isActive).length,
      totalApplications,
      statusCounts
    });
  } catch (err) {
    return res.status(500).json({ message: 'Failed to fetch stats', error: err.message });
  }
});

module.exports = router;
