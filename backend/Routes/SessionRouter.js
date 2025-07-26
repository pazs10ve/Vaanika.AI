const express = require('express');
const router = express.Router();
const Session = require('../Models/Session');
const ensureAuthenticated = require('../Middlewares/Auth');

// Apply authentication middleware to all routes
router.use(ensureAuthenticated);

// POST /api/sessions - Create a new session
router.post('/', async (req, res) => {
  try {
    const { title, userName } = req.body;
    const userId = req.user._id; // Get userId from JWT token

    if (!title || !userName) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const session = new Session({ title, userId, userName });
    await session.save();

    res.status(201).json(session);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create session' });
  }
});

// GET /api/sessions - List all sessions for the authenticated user
router.get('/', async (req, res) => {
  try {
    const userId = req.user._id; // Get userId from JWT token
    const sessions = await Session.find({ userId });
    res.json(sessions);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch sessions' });
  }
});

// GET /api/sessions/:id/messages - Get all messages for a session
router.get('/:id/messages', async (req, res) => {
  try {
    const session = await Session.findById(req.params.id);
    if (!session) {
      return res.status(404).json({ error: 'Session not found' });
    }
    // Ensure only the owner can access
    if (session.userId !== req.user._id) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    res.json(session.messages);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch messages' });
  }
});

module.exports = router;
