const { User } = require('../models');

/**
 * PUT /user/profile - Update current user's profile information
 * Allows updating nickname and avatar_url.
 */
async function updateUserProfile(req, res) {
  const userId = req.user.id; // From authenticateToken middleware
  const { nickname, avatar_url } = req.body;

  const updatesToApply = {};
  if (nickname !== undefined) {
    if (typeof nickname !== 'string' || nickname.trim() === '') {
      return res.status(400).json({ message: 'Nickname, if provided, must be a non-empty string.' });
    }
    updatesToApply.nickname = nickname.trim();
  }

  if (avatar_url !== undefined) {
    if (typeof avatar_url !== 'string' || avatar_url.trim() === '') {
      // Allow setting avatar_url to empty string to remove it, or validate URL format
      updatesToApply.avatar_url = avatar_url.trim();
    } else {
       // Basic URL validation (optional, can be more robust)
      try {
        new URL(avatar_url); // This will throw if invalid URL
        updatesToApply.avatar_url = avatar_url;
      } catch (e) {
        return res.status(400).json({ message: 'Avatar URL, if provided, must be a valid URL.' });
      }
    }
  }

  // Add other updatable fields here if any (e.g., bio, custom_status)
  // For example:
  // if (req.body.bio !== undefined) {
  //   updatesToApply.bio = req.body.bio;
  // }

  if (Object.keys(updatesToApply).length === 0) {
    return res.status(400).json({ message: 'No valid fields provided for update.' });
  }

  try {
    const user = await User.findByPk(userId);
    if (!user) {
      // Should not happen if token is valid and user exists from auth middleware
      return res.status(404).json({ message: 'User not found.' });
    }

    await user.update(updatesToApply);

    // Return updated user profile (excluding sensitive info)
    const userDetail = {
      id: user.id,
      openid: user.openid, // Typically not changed by user
      nickname: user.nickname,
      avatar_url: user.avatar_url,
      gender: user.gender,
      country: user.country,
      province: user.province,
      city: user.city,
      // bio: user.bio, // if added
    };

    return res.status(200).json({ message: 'Profile updated successfully.', userDetail });

  } catch (error) {
    console.error(`Error updating profile for user ${userId}:`, error);
    if (error.name === 'SequelizeValidationError') {
      return res.status(400).json({ message: 'Validation error updating profile.', errors: error.errors.map(e => e.message) });
    }
    return res.status(500).json({ message: 'Failed to update profile.', error: error.message });
  }
}

/**
 * GET /user/profile - Get current user's profile information
 */
async function getUserProfile(req, res) {
    const userId = req.user.id;
    try {
        // req.user is already populated by authenticateToken middleware with selected fields.
        // If you need to fetch more fields or ensure latest data:
        // const user = await User.findByPk(userId, {
        //   attributes: ['id', 'openid', 'nickname', 'avatar_url', 'gender', 'country', 'province', 'city' /*, 'bio' */]
        // });
        // if (!user) {
        //   return res.status(404).json({ message: 'User not found.' });
        // }
        // return res.status(200).json(user);

        // Using req.user directly (as populated by authMiddleware)
        return res.status(200).json(req.user);

    } catch (error) {
        console.error(`Error fetching profile for user ${userId}:`, error);
        return res.status(500).json({ message: 'Failed to fetch user profile.', error: error.message });
    }
}


module.exports = {
  updateUserProfile,
  getUserProfile,
};
