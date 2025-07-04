const qiniu = require('qiniu');
require('dotenv').config();

const QINIU_ACCESS_KEY = process.env.QINIU_ACCESS_KEY;
const QINIU_SECRET_KEY = process.env.QINIU_SECRET_KEY;
const QINIU_BUCKET = process.env.QINIU_BUCKET;
// const QINIU_DOMAIN = process.env.QINIU_DOMAIN; // Domain might be needed for constructing URLs, but not for token itself

/**
 * Generates an upload token for Qiniu Cloud Storage.
 * @param {string} [keyToOverwrite=null] - Optional. If specified, the token allows overwriting this specific key.
 * @param {number} [expires=3600] - Optional. Token validity duration in seconds. Defaults to 1 hour.
 * @returns {string} The generated upload token.
 * @throws {Error} If Qiniu credentials are not configured or if token generation fails.
 */
function getUploadToken(keyToOverwrite = null, expires = 3600) {
  if (!QINIU_ACCESS_KEY || !QINIU_SECRET_KEY || !QINIU_BUCKET) {
    throw new Error('Qiniu OSS credentials (Access Key, Secret Key, Bucket) are not fully configured in .env file.');
  }

  const mac = new qiniu.auth.digest.Mac(QINIU_ACCESS_KEY, QINIU_SECRET_KEY);

  const options = {
    scope: QINIU_BUCKET,
    expires: expires, // Token validity in seconds
    // returnBody: '{"key":"$(key)","hash":"$(etag)","fsize":$(fsize),"bucket":"$(bucket)","name":"$(x:name)"}', // Optional: define what Qiniu returns to client after upload
    // callbackUrl: 'YOUR_CALLBACK_URL', // Optional: Qiniu server sends callback to this URL after upload
    // callbackBody: 'key=$(key)&hash=$(etag)', // Optional: content of the callback
    // callbackBodyType: 'application/x-www-form-urlencoded' // Optional: callback content type
  };

  // If keyToOverwrite is provided, the token will be for overwriting that specific file.
  // If client uploads with a key that matches this, it will overwrite.
  // If client uploads without a key, Qiniu will generate one (usually hash-based).
  // If client uploads with a different key, it will create a new file with that key.
  // For a general purpose token where client specifies the key or Qiniu generates it:
  // scope should just be the bucket name.
  // If you want to force the client to upload with a specific key, or allow overwriting a specific key:
  if (keyToOverwrite) {
    options.scope = `${QINIU_BUCKET}:${keyToOverwrite}`;
  }

  const putPolicy = new qiniu.rs.PutPolicy(options);
  const uploadToken = putPolicy.uploadToken(mac);

  if (!uploadToken) {
    // This case should ideally not happen if qiniu SDK works correctly and options are valid
    throw new Error('Failed to generate Qiniu upload token.');
  }

  return uploadToken;
}

module.exports = {
  getUploadToken,
};
