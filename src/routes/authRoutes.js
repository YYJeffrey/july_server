const express = require('express');
const authController = require('../controllers/authController');

const router = express.Router();

// POST /api/auth/passive - For passive (silent) login or session renewal
router.post('/passive', authController.passiveLogin);

// POST /api/auth/initiative - For user-initiated login with profile data authorization
router.post('/initiative', authController.initiativeLogin); // Placeholder, will be implemented later

module.exports = router;
