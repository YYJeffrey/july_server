const { ChatMessage, User } = require('../models'); // Assuming User model might be needed for sender details
const { Op } = require('sequelize');

/**
 * GET /chat - Load historical chat messages for a room with pagination.
 * Query params:
 * - room_id: string, required. The ID of the chat room.
 * - before_message_id: bigint, optional. To fetch messages older than this message ID (cursor).
 * - limit: int, optional. Number of messages to fetch (e.g., 20). Defaults to 20.
 */
async function getChatHistory(req, res) {
  const { room_id, before_message_id, limit = 20 } = req.query;
  const userId = req.user.id; // Authenticated user making the request

  if (!room_id) {
    return res.status(400).json({ message: 'room_id query parameter is required.' });
  }

  const queryOptions = {
    where: {
      room_id,
    },
    order: [['created_at', 'DESC']], // Get newest first, then reverse on client if needed, or sort ASC and take last N. For "load older", DESC is better.
    limit: parseInt(limit, 10) || 20,
    include: [
      {
        model: User,
        as: 'sender',
        attributes: ['id', 'nickname', 'avatar_url'], // Select specific attributes for sender
      },
    ],
  };

  if (before_message_id) {
    // To fetch messages older than a certain message_id, we need their created_at timestamp.
    // Or, if IDs are sequential and time-ordered (like auto-increment bigint), we can use ID directly.
    // Assuming ID is a reliable cursor for "older than".
    queryOptions.where.id = { [Op.lt]: before_message_id };
  }

  // Security check: Ensure the requesting user is part of this room_id.
  // For private chats (e.g., room_id = 'userA_userB'), check if req.user.id is one of them.
  // For group chats, this would involve checking group membership (not implemented yet).
  // Basic check for private chat format:
  if (room_id.includes('_')) { // Potential private chat
    const participants = room_id.split('_');
    if (!participants.includes(String(userId))) {
        // Check if user is part of a group if group logic existed
        // For now, if it looks like a private chat and user is not part of it, deny.
        console.warn(`User ${userId} attempted to access chat history for room ${room_id} they are not part of.`);
        return res.status(403).json({ message: 'Forbidden: You do not have access to this chat room.' });
    }
  } // Else, it might be a group chat ID. Access control for groups would be more complex.


  try {
    const messages = await ChatMessage.findAll(queryOptions);

    // For anonymous messages, ensure sender details are masked if the requester is not an admin/special role.
    // The `is_anonymous` flag is already on the message. Client can use it.
    // If backend needs to enforce masking for API responses:
    const processedMessages = messages.map(msg => {
      const messageJson = msg.toJSON();
      if (messageJson.is_anonymous) {
        // Even if we joined User model, override sender details for anonymous messages.
        messageJson.sender = { id: null, nickname: 'Anonymous', avatar_url: null };
      }
      // For 'is_burn' messages, the client is expected to handle the "burn" effect.
      // If server-side logic for "already burned" was needed, it would be more complex (e.g., tracking read status).
      return messageJson;
    });

    // Messages are currently newest-first due to ORDER BY created_at DESC.
    // Client typically wants oldest-first for display, or to prepend older messages.
    // So, reversing here makes it easier for client to append/prepend.
    return res.status(200).json(processedMessages.reverse());

  } catch (error) {
    console.error(`Error fetching chat history for room ${room_id}:`, error);
    return res.status(500).json({ message: 'Failed to fetch chat history.', error: error.message });
  }
}

module.exports = {
  getChatHistory,
};
