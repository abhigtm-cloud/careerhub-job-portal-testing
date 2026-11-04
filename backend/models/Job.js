const mongoose = require('mongoose');

const jobSchema = new mongoose.Schema(
  {
    title: { type: String, required: true, trim: true, maxlength: 120 },
    company: { type: String, required: true, trim: true, maxlength: 100 },
    location: { type: String, default: 'Remote', maxlength: 100 },
    employmentType: {
      type: String,
      enum: ['Full-time', 'Part-time', 'Internship', 'Contract'],
      default: 'Full-time'
    },
    experienceLevel: {
      type: String,
      enum: ['Fresher', 'Junior', 'Mid', 'Senior', 'Lead'],
      default: 'Fresher'
    },
    skills: { type: [String], default: [] },
    description: { type: String, required: true, maxlength: 4000 },
    requirements: { type: [String], default: [] },
    salaryMin: { type: Number, default: 0, min: 0 },
    salaryMax: { type: Number, default: 0, min: 0 },
    postedBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    isActive: { type: Boolean, default: true }
  },
  { timestamps: true }
);

jobSchema.index({ title: 'text', company: 'text', skills: 'text' });

module.exports = mongoose.model('Job', jobSchema);
