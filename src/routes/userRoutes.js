const express = require('express');
const userController = require('../controllers/userController');
const { authenticateToken } = require('../middlewares/authMiddleware');

const router = express.Router();

// GET /api/user/profile - Get current user's profile
// All routes in this file are authenticated
router.use(authenticateToken);

router.get('/profile', userController.getUserProfile);

// PUT /api/user/profile - Update current user's profile
router.put('/profile', userController.updateUserProfile);

// Example for other user-related routes if needed in future:
// router.get('/:userId/profile', someController.getSpecificUserProfile); // e.g., view other user's public profile

module.exports = router;
