require('dotenv').config({ path: require('path').join(__dirname, '..', '.env') });
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const connectDB = require('../config/db');
const User = require('../models/User');
const Job = require('../models/Job');

const CANDIDATE_EMAIL = 'candidate@careerhub.com';
const RECRUITER_EMAIL = 'recruiter@careerhub.com';
const DEMO_PASSWORD = 'CareerHub@123';

const JOB_SEEDS = [
  {
    title: 'Frontend Developer (React)',
    company: 'Nimbus Technologies',
    location: 'Bengaluru, India',
    employmentType: 'Full-time',
    experienceLevel: 'Junior',
    skills: ['React', 'JavaScript', 'CSS', 'Bootstrap'],
    description: 'Build and maintain responsive user interfaces for our SaaS analytics dashboard using React and Bootstrap.',
    requirements: ['1-2 years with React', 'Strong CSS fundamentals', 'Familiarity with REST APIs'],
    salaryMin: 600000,
    salaryMax: 900000
  },
  {
    title: 'Backend Engineer (Node.js)',
    company: 'Orbit Systems',
    location: 'Hyderabad, India',
    employmentType: 'Full-time',
    experienceLevel: 'Mid',
    skills: ['Node.js', 'Express', 'MongoDB', 'REST APIs'],
    description: 'Design and build scalable REST APIs powering our logistics platform, working closely with the product team.',
    requirements: ['3+ years backend experience', 'Experience with MongoDB or similar NoSQL DB', 'Understanding of JWT auth'],
    salaryMin: 1000000,
    salaryMax: 1500000
  },
  {
    title: 'Full Stack Intern',
    company: 'Brightline Labs',
    location: 'Remote',
    employmentType: 'Internship',
    experienceLevel: 'Fresher',
    skills: ['JavaScript', 'React', 'Node.js'],
    description: 'Six-month internship building features end-to-end across our React frontend and Node backend, with mentorship.',
    requirements: ['Final-year student or recent graduate', 'Basic knowledge of JS/React', 'Eagerness to learn'],
    salaryMin: 15000,
    salaryMax: 25000
  },
  {
    title: 'DevOps Engineer',
    company: 'Vertex Cloud',
    location: 'Pune, India',
    employmentType: 'Full-time',
    experienceLevel: 'Senior',
    skills: ['AWS', 'Docker', 'Kubernetes', 'CI/CD'],
    description: 'Own our CI/CD pipelines and cloud infrastructure, improving reliability and deployment speed across services.',
    requirements: ['5+ years in DevOps/SRE roles', 'Hands-on AWS and Kubernetes experience', 'Scripting in Python or Bash'],
    salaryMin: 1800000,
    salaryMax: 2600000
  },
  {
    title: 'QA Automation Engineer',
    company: 'Quanta Software',
    location: 'Chandigarh, India',
    employmentType: 'Full-time',
    experienceLevel: 'Junior',
    skills: ['Python', 'Selenium', 'Pytest', 'API Testing'],
    description: 'Build and maintain automated test suites for our web applications using Python, Selenium and Pytest.',
    requirements: ['1+ years in test automation', 'Experience with Selenium WebDriver', 'Understanding of REST API testing'],
    salaryMin: 500000,
    salaryMax: 750000
  },
  {
    title: 'Product Designer (UI/UX)',
    company: 'Nimbus Technologies',
    location: 'Bengaluru, India',
    employmentType: 'Full-time',
    experienceLevel: 'Mid',
    skills: ['Figma', 'UI Design', 'UX Research'],
    description: 'Lead end-to-end design for new product modules, from research and wireframes to high-fidelity prototypes.',
    requirements: ['3+ years product design experience', 'Strong Figma portfolio', 'Comfortable working with engineers'],
    salaryMin: 900000,
    salaryMax: 1300000
  },
  {
    title: 'Data Analyst',
    company: 'Orbit Systems',
    location: 'Remote',
    employmentType: 'Contract',
    experienceLevel: 'Junior',
    skills: ['SQL', 'Python', 'Data Visualization'],
    description: 'Analyze operational data and build dashboards that help stakeholders make data-driven decisions.',
    requirements: ['Strong SQL skills', 'Experience with Python pandas', 'Ability to communicate insights clearly'],
    salaryMin: 50000,
    salaryMax: 70000
  },
  {
    title: 'Engineering Lead',
    company: 'Vertex Cloud',
    location: 'Gurugram, India',
    employmentType: 'Full-time',
    experienceLevel: 'Lead',
    skills: ['Leadership', 'Node.js', 'System Design', 'React'],
    description: 'Lead a team of 6 engineers building our customer-facing platform, owning architecture and delivery.',
    requirements: ['7+ years engineering experience', '2+ years in a lead role', 'Strong system design fundamentals'],
    salaryMin: 2800000,
    salaryMax: 4000000
  }
];

async function run() {
  await connectDB();

  let candidate = await User.findOne({ email: CANDIDATE_EMAIL });
  if (!candidate) {
    const passwordHash = await bcrypt.hash(DEMO_PASSWORD, 10);
    candidate = await User.create({
      name: 'Demo Candidate',
      email: CANDIDATE_EMAIL,
      passwordHash,
      role: 'candidate',
      headline: 'Aspiring Full Stack Developer',
      phone: '9876543210',
      skills: ['JavaScript', 'React', 'Node.js']
    });
    console.log(`[seed] created candidate ${CANDIDATE_EMAIL}`);
  } else {
    console.log(`[seed] candidate ${CANDIDATE_EMAIL} already exists, skipping`);
  }

  let recruiter = await User.findOne({ email: RECRUITER_EMAIL });
  if (!recruiter) {
    const passwordHash = await bcrypt.hash(DEMO_PASSWORD, 10);
    recruiter = await User.create({
      name: 'Demo Recruiter',
      email: RECRUITER_EMAIL,
      passwordHash,
      role: 'recruiter',
      company: 'Nimbus Technologies'
    });
    console.log(`[seed] created recruiter ${RECRUITER_EMAIL}`);
  } else {
    console.log(`[seed] recruiter ${RECRUITER_EMAIL} already exists, skipping`);
  }

  const existingJobCount = await Job.countDocuments({ postedBy: recruiter._id });
  if (existingJobCount === 0) {
    const jobs = JOB_SEEDS.map((job) => ({ ...job, postedBy: recruiter._id }));
    await Job.insertMany(jobs);
    console.log(`[seed] inserted ${jobs.length} job listings`);
  } else {
    console.log(`[seed] jobs already seeded for recruiter (${existingJobCount} found), skipping`);
  }

  console.log('[seed] done');
  console.log(`[seed] demo credentials -> candidate: ${CANDIDATE_EMAIL} / ${DEMO_PASSWORD}`);
  console.log(`[seed] demo credentials -> recruiter: ${RECRUITER_EMAIL} / ${DEMO_PASSWORD}`);

  await mongoose.disconnect();
}

run().catch((err) => {
  console.error('[seed] failed:', err);
  process.exit(1);
});
