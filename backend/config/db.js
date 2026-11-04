const mongoose = require('mongoose');

async function connectDB() {
  const uri = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/careerhub';
  await mongoose.connect(uri);
  console.log(`[db] connected to ${uri}`);
}

module.exports = connectDB;
