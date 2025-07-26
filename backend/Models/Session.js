// models/Session.js
const mongoose = require('mongoose');

const SessionSchema = new mongoose.Schema({
  title: { type: String, required: true },
  userId: { type: String, required: true }, // User ID for privacy
  userName: { type: String, required: true }, // User name for display
  messages: [{ 
    role: { type: String, enum: ['user', 'assistant'], required: true },
    content: { type: String, required: true },
    type: { type: String, enum: ['video', 'audio', 'graphics'] },
    timestamp: { type: Date, default: Date.now }
  }],
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Session', SessionSchema);
