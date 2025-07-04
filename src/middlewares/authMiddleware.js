const { verifyToken } = require('../utils/jwtUtils');
const { User } = require('../models');

/**
 * Middleware to authenticate users via JWT.
 * If token is valid, it attaches the user object (without sensitive info) to req.user.
 */
async function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.startsWith('Bearer ') && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ message: 'Unauthorized: No token provided.' });
  }

  const decodedPayload = verifyToken(token);

  if (!decodedPayload || !decodedPayload.userId) {
    return res.status(403).json({ message: 'Forbidden: Invalid or expired token.' });
  }

  try {
    // Fetch user from DB to ensure they still exist and are active, etc.
    // You might want to select only specific attributes.
    const user = await User.findByPk(decodedPayload.userId, {
      attributes: ['id', 'openid', 'nickname', 'avatar_url', 'gender'] // Exclude sensitive fields like session_key
    });

    if (!user) {
      return res.status(403).json({ message: 'Forbidden: User not found.' });
    }

    req.user = user; // Attach user object to the request
    next();
  } catch (error) {
    console.error('Error fetching user during authentication:', error);
    return res.status(500).json({ message: 'Internal server error during authentication.' });
  }
}

module.exports = {
  authenticateToken,
};
