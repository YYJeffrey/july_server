const express = require('express');
const ossController = require('../controllers/ossController');
const { authenticateToken } = require('../middlewares/authMiddleware'); // Assuming token generation should be an authenticated action

const router = express.Router();

// GET /api/oss/qiniu_token - Get Qiniu upload token
// Protected route: only authenticated users can get an upload token.
router.get('/qiniu_token', authenticateToken, ossController.getQiniuUploadToken);

module.exports = router;
