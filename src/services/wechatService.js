const axios = require('axios');
require('dotenv').config();

const WECHAT_APPID = process.env.WECHAT_APPID;
const WECHAT_SECRET = process.env.WECHAT_SECRET;

/**
 * Exchanges a WeChat login code for a session key and openid.
 * @param {string} code - The login code from wx.login().
 * @returns {Promise<object>} An object containing openid and session_key.
 * @throws {Error} If the request to WeChat API fails or returns an error.
 */
async function codeToSession(code) {
  if (!WECHAT_APPID || !WECHAT_SECRET) {
    throw new Error('WeChat AppID or Secret is not configured in .env file.');
  }

  const url = `https://api.weixin.qq.com/sns/jscode2session?appid=${WECHAT_APPID}&secret=${WECHAT_SECRET}&js_code=${code}&grant_type=authorization_code`;

  try {
    const response = await axios.get(url);
    const data = response.data;

    if (data.errcode && data.errcode !== 0) {
      throw new Error(`WeChat API Error: ${data.errmsg} (errcode: ${data.errcode})`);
    }

    if (!data.openid || !data.session_key) {
      throw new Error('Failed to retrieve openid or session_key from WeChat.');
    }

    return {
      openid: data.openid,
      session_key: data.session_key,
      unionid: data.unionid // Optional, may not be present
    };
  } catch (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Error response from WeChat API:', error.response.data);
      throw new Error(`WeChat API request failed with status ${error.response.status}: ${error.response.data.errmsg || 'Unknown error'}`);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received from WeChat API:', error.request);
      throw new Error('No response received from WeChat API. Check network connectivity.');
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error setting up WeChat API request:', error.message);
      throw new Error(error.message); // Propagate original error or a more specific one
    }
  }
}

/**
 * Decrypts WeChat encrypted data.
 * Note: This is a placeholder. The actual decryption logic using crypto module is needed.
 * The 'crypto' module is a built-in Node.js module.
 * @param {string} encryptedData - The encrypted data from WeChat.
 * @param {string} sessionKey - The session_key obtained from codeToSession.
 * @param {string} iv - The initialization vector.
 * @returns {object} The decrypted user information.
 * @throws {Error} If decryption fails.
 */
function decryptData(encryptedData, sessionKey, iv) {
  // Placeholder for actual decryption logic using Node.js crypto module
  // This typically involves:
  // 1. Base64 decoding sessionKey, encryptedData, iv.
  // 2. Creating a decipher using 'aes-128-cbc' algorithm, the decoded sessionKey, and decoded iv.
  // 3. Updating the decipher with the decoded encryptedData.
  // 4. Finalizing the decipher.
  // 5. Parsing the result as JSON.
  const crypto = require('crypto'); // Ensure crypto is required

  try {
    const sessionKeyDecoded = Buffer.from(sessionKey, 'base64');
    const encryptedDataDecoded = Buffer.from(encryptedData, 'base64');
    const ivDecoded = Buffer.from(iv, 'base64');

    // Create decipher object
    // Algorithm: aes-128-cbc
    // Key: sessionKey (decoded from base64)
    // IV: iv (decoded from base64)
    let decipher = crypto.createDecipheriv('aes-128-cbc', sessionKeyDecoded, ivDecoded);

    // Disable auto padding, WeChat docs sometimes imply pkcs#7 padding which is handled by default if auto padding is true.
    // However, explicit control might be needed if issues arise.
    // For now, let's assume auto padding (true by default) works. If not, setAutoPadding(false) and handle padding manually.
    decipher.setAutoPadding(true);

    let decoded = decipher.update(encryptedDataDecoded, 'binary', 'utf8');
    decoded += decipher.final('utf8');

    const decryptedUserInfo = JSON.parse(decoded);

    // Validate appid in watermark to ensure data integrity and origin
    if (decryptedUserInfo.watermark && decryptedUserInfo.watermark.appid !== WECHAT_APPID) {
      console.error('Decrypted data watermark appid mismatch.', {
        expectedAppId: WECHAT_APPID,
        actualAppId: decryptedUserInfo.watermark.appid
      });
      throw new Error('Invalid AppID in decrypted data watermark. Data may be tampered or from wrong source.');
    }
    return decryptedUserInfo;

  } catch (err) {
    console.error("Decryption failed:", err.message, err.stack);
    // More specific error messages based on error type if possible
    if (err.message.includes('bad decrypt') || err.message.includes('mac check failed')) {
        throw new Error('Failed to decrypt WeChat data: Invalid session key or IV, or data corrupted.');
    } else if (err.message.includes('Invalid IV length')) {
        throw new Error('Failed to decrypt WeChat data: Invalid IV length.');
    }
    throw new Error('Failed to decrypt WeChat data. Ensure session_key, encryptedData, and iv are correct.');
  }
}

module.exports = {
  codeToSession,
  decryptData
};
