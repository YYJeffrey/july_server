const { User } = require('../models'); // Sequelize User model
const wechatService = require('../services/wechatService');
const { generateToken } = require('../utils/jwtUtils');
require('dotenv').config();

/**
 * Handles passive login (wx.login code exchange)
 * POST /auth/passive
 */
async function passiveLogin(req, res) {
  const { code } = req.body;

  if (!code) {
    return res.status(400).json({ message: 'Login code (code) is required.' });
  }

  try {
    // 1. Exchange code for openid and session_key
    const { openid, session_key, unionid } = await wechatService.codeToSession(code);

    // 2. Find user by openid or create a new one
    let user = await User.findOne({ where: { openid } });

    if (!user) {
      // Create a new user with minimal information
      // More details (nickname, avatar_url) can be added via initiative login or profile update
      user = await User.create({
        openid,
        session_key, // Storing session_key; consider security implications (e.g., encryption at rest)
        // nickname: null, // Defaulted by model
        // avatar_url: null, // Defaulted by model
        // gender: null, // Defaulted by model
      });
    } else {
      // If user exists, update session_key (it might change)
      user.session_key = session_key;
      await user.save();
    }

    // 3. Prepare user detail for response (do not send session_key to client)
    const userDetail = {
      id: user.id,
      openid: user.openid,
      nickname: user.nickname,
      avatar_url: user.avatar_url,
      gender: user.gender,
      // Add any other fields from the user model that are safe to return
    };

    // 4. Generate JWT token
    const tokenPayload = {
      userId: user.id,
      openid: user.openid,
    };
    const token = generateToken(tokenPayload);

    // 5. Return token and userDetail
    return res.status(200).json({
      message: 'Login successful.',
      token,
      userDetail,
    });

  } catch (error) {
    console.error('Passive login error:', error);
    // Distinguish WeChat API errors from other server errors if possible
    if (error.message.startsWith('WeChat API Error:') || error.message.startsWith('Failed to retrieve openid')) {
      return res.status(502).json({ message: 'WeChat API request failed.', error: error.message });
    }
    if (error.message === 'WeChat AppID or Secret is not configured in .env file.') {
        return res.status(500).json({ message: 'Server configuration error for WeChat integration.' });
    }
    return res.status(500).json({ message: 'Internal server error during login.', error: error.message });
  }
}

// Placeholder for initiativeLogin
async function initiativeLogin(req, res) {
  const { code, encryptedData, iv } = req.body;

  if (!code || !encryptedData || !iv) {
    return res.status(400).json({ message: 'Request must include code, encryptedData, and iv.' });
  }

  try {
    // 1. Exchange code for openid and session_key
    // It's important to get a fresh session_key with each initiative login attempt using the new code,
    // as session_keys can expire or be invalidated.
    const { openid, session_key } = await wechatService.codeToSession(code);

    // 2. Decrypt user info
    const decryptedUserInfo = wechatService.decryptData(encryptedData, session_key, iv);

    // Validate that the openid from decrypted data matches the one from codeToSession
    // This is a crucial security check.
    if (decryptedUserInfo.openId !== openid && decryptedUserInfo.openId !== decryptedUserInfo.unionId) { // Check openId first, then unionId if openId is not primary identifier in decrypted data
        // WeChat sometimes returns openId and sometimes openid in the decrypted data.
        // Also, if unionId mechanism is active, openId in decrypted data might be the unionId.
        // The primary identifier from codeToSession is `openid`.
        // This check needs to be robust against WeChat's varying field names.
        // Let's assume `decryptedUserInfo.openId` or `decryptedUserInfo.openid` is what we need to check.
        const decryptedOpenIdField = decryptedUserInfo.openId || decryptedUserInfo.openid;
        if (decryptedOpenIdField !== openid) {
            console.error('OpenID mismatch between codeToSession and decrypted data.', {
                codeToSessionOpenId: openid,
                decryptedOpenId: decryptedOpenIdField,
                decryptedUnionId: decryptedUserInfo.unionId
            });
            throw new Error('OpenID mismatch. Data integrity compromised.');
        }
    }


    // 3. Find user by openid. User should ideally exist from a passive login,
    //    but if not (e.g., first login is initiative), create them.
    let user = await User.findOne({ where: { openid } });

    if (!user) {
      // This case might happen if initiative login is the very first interaction.
      user = await User.create({
        openid,
        session_key, // Store the new session_key
        nickname: decryptedUserInfo.nickName,
        avatar_url: decryptedUserInfo.avatarUrl,
        gender: decryptedUserInfo.gender,
        country: decryptedUserInfo.country,
        province: decryptedUserInfo.province,
        city: decryptedUserInfo.city,
        // unionid: decryptedUserInfo.unionId, // If you have a unionid column
      });
    } else {
      // Update user with new information and session_key
      user.session_key = session_key; // Always update to the latest session_key
      user.nickname = decryptedUserInfo.nickName;
      user.avatar_url = decryptedUserInfo.avatarUrl;
      user.gender = decryptedUserInfo.gender;
      user.country = decryptedUserInfo.country;
      user.province = decryptedUserInfo.province;
      user.city = decryptedUserInfo.city;
      // if (decryptedUserInfo.unionId) user.unionid = decryptedUserInfo.unionId;
      await user.save();
    }

    // 4. Prepare user detail for response
    const userDetail = {
      id: user.id,
      openid: user.openid,
      nickname: user.nickname,
      avatar_url: user.avatar_url,
      gender: user.gender,
      // unionid: user.unionid, // if applicable
    };

    // 5. Generate JWT token
    const tokenPayload = {
      userId: user.id,
      openid: user.openid,
    };
    const token = generateToken(tokenPayload);

    // 6. Return token and userDetail
    return res.status(200).json({
      message: 'Initiative login successful. User info updated.',
      token,
      userDetail,
    });

  } catch (error) {
    console.error('Initiative login error:', error);
    if (error.message.includes('WeChat API Error') || error.message.includes('Failed to retrieve') || error.message.includes('Failed to decrypt')) {
      return res.status(502).json({ message: 'WeChat service error.', error: error.message });
    }
    if (error.message === 'WeChat AppID or Secret is not configured in .env file.') {
        return res.status(500).json({ message: 'Server configuration error for WeChat integration.' });
    }
    if (error.message === 'OpenID mismatch. Data integrity compromised.') {
        return res.status(400).json({ message: 'Data validation failed.', error: error.message });
    }
    return res.status(500).json({ message: 'Internal server error during initiative login.', error: error.message });
  }
}


module.exports = {
  passiveLogin,
  initiativeLogin,
};
