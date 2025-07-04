const jwt = require('jsonwebtoken');
require('dotenv').config();

const JWT_SECRET = process.env.JWT_SECRET;
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '1d';

if (!JWT_SECRET) {
  throw new Error('JWT_SECRET is not defined in your .env file. Please add it.');
}

/**
 * Generates a JWT token.
 * @param {object} payload - The payload to include in the token (e.g., userId, openid).
 * @returns {string} The generated JWT token.
 */
function generateToken(payload) {
  if (!payload || typeof payload !== 'object' || Object.keys(payload).length === 0) {
    throw new Error('Payload must be a non-empty object.');
  }
  return jwt.sign(payload, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });
}

/**
 * Verifies a JWT token.
 * @param {string} token - The JWT token to verify.
 * @returns {object|null} The decoded payload if verification is successful, otherwise null.
 */
function verifyToken(token) {
  if (!token) {
    return null;
  }
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (error) {
    console.error('JWT Verification Error:', error.message);
    return null;
  }
}

module.exports = {
  generateToken,
  verifyToken,
};
