const mongoose = require('mongoose');

const userSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true, minlength: 2, maxlength: 80 },
    email: { type: String, required: true, unique: true, lowercase: true, trim: true },
    passwordHash: { type: String, required: true },
    role: { type: String, enum: ['candidate', 'recruiter'], required: true },
    headline: { type: String, default: '', maxlength: 120 },
    phone: { type: String, default: '', maxlength: 20 },
    skills: { type: [String], default: [] },
    company: { type: String, default: '', maxlength: 100 }
  },
  { timestamps: true }
);

module.exports = mongoose.model('User', userSchema);
