const express = require('express');
const chatApiController = require('../controllers/chatApiController');
const { authenticateToken } = require('../middlewares/authMiddleware');

const router = express.Router();

// GET /api/chat - Get chat history for a room
// Protected route: only authenticated users can fetch chat history.
router.get('/', authenticateToken, chatApiController.getChatHistory);

module.exports = router;
