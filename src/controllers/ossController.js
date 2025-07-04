const qiniuService = require('../services/qiniuService');

/**
 * Controller to get Qiniu Upload Token
 * GET /oss/qiniu_token
 */
async function getQiniuUploadToken(req, res) {
  try {
    // Optional: if you want to generate a token for a specific file key (e.g., for overwriting)
    // const { key } = req.query; // Example: /oss/qiniu_token?key=my-specific-file.jpg
    // const token = qiniuService.getUploadToken(key);

    // For a general purpose token:
    const token = qiniuService.getUploadToken();

    return res.status(200).json({
      message: 'Qiniu upload token generated successfully.',
      uptoken: token, // Standard field name for Qiniu upload token
    });

  } catch (error) {
    console.error('Error generating Qiniu upload token:', error);
    if (error.message.includes('Qiniu OSS credentials')) {
      return res.status(500).json({ message: 'Server configuration error for Qiniu integration.' });
    }
    return res.status(500).json({ message: 'Failed to generate Qiniu upload token.', error: error.message });
  }
}

module.exports = {
  getQiniuUploadToken,
};
