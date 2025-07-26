const express = require('express');
const router = express.Router();
const Session = require('../Models/Session');
const ensureAuthenticated = require('../Middlewares/Auth');

// Apply authentication middleware to all routes
router.use(ensureAuthenticated);

// Mock response
const mockAIResponse = async (prompt, type) => {
  return {
    type,
    content: `Generated ${type} from: "${prompt}"`,
  };
};

// General handler
const handleGeneration = (type) => async (req, res) => {
  try {
    const { sessionId, prompt } = req.body;
    if (!sessionId || !prompt) {
      return res.status(400).json({ error: 'sessionId and prompt are required' });
    }

    const session = await Session.findById(sessionId);
    if (!session) {
      console.error('Session not found:', sessionId);
      return res.status(404).json({ error: 'Session not found' });
    }

    const userMessage = { role: 'user', content: prompt, type };
    const aiResponse = await mockAIResponse(prompt, type);
    const assistantMessage = { role: 'assistant', content: aiResponse.content, type };

    session.messages.push(userMessage, assistantMessage);
    await session.save();

    res.json({ response: assistantMessage });
  } catch (error) {
    console.error(`[${type.toUpperCase()}] Error:`, error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

router.post('/video', handleGeneration('video'));
router.post('/audio', handleGeneration('audio'));
router.post('/graphics', handleGeneration('graphics'));

module.exports = router;
