const express = require('express');
const http = require('http');
const { Server } = require("socket.io");
const cors = require('cors');
require('dotenv').config();

const { sequelize } = require('./models');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/api/health', (req, res) => { // Changed to /api/health for a common health check endpoint
  res.status(200).json({ status: 'UP', message: 'Ginco MiniApp Backend is running.' });
});

// Placeholder for routes
const authRoutes = require('./routes/authRoutes');
app.use('/api/auth', authRoutes);
const eventRoutes = require('./routes/eventRoutes');
app.use('/api/events', eventRoutes);
const chatApiRoutes = require('./routes/chatApiRoutes');
app.use('/api/chat', chatApiRoutes);
const ossRoutes = require('./routes/ossRoutes');
app.use('/api/oss', ossRoutes);
const userRoutes = require('./routes/userRoutes'); // Add this
app.use('/api/user', userRoutes); // Add this

// In-memory store for user socket connections (socket.id -> userId)
// Consider Redis for multi-instance deployments
const userSockets = new Map();
const { verifyToken } = require('./utils/jwtUtils'); // For Socket.IO auth

io.use(async (socket, next) => { // Socket.IO middleware for authentication
  const token = socket.handshake.auth.token;
  if (!token) {
    console.log(`Socket ${socket.id} connection rejected: No token provided.`);
    return next(new Error('Authentication error: No token provided.'));
  }

  const decodedPayload = verifyToken(token);
  if (!decodedPayload || !decodedPayload.userId) {
    console.log(`Socket ${socket.id} connection rejected: Invalid or expired token.`);
    return next(new Error('Authentication error: Invalid or expired token.'));
  }

  try {
    // Optional: Fetch user from DB to ensure they still exist, similar to API auth middleware
    // For socket connections, often the userId from a valid token is trusted for performance.
    // If DB check is needed:
    // const user = await User.findByPk(decodedPayload.userId);
    // if (!user) {
    //   return next(new Error('Authentication error: User not found.'));
    // }
    // socket.user = user.toJSON(); // Attach user to socket, excluding sensitive data

    socket.user = { id: decodedPayload.userId, openid: decodedPayload.openid }; // Attach basic user info from token
    console.log(`Socket ${socket.id} authenticated for user ${socket.user.id}`);
    next();
  } catch (error) {
    console.error(`Socket ${socket.id} authentication error:`, error);
    return next(new Error('Authentication error: Server error during authentication.'));
  }
});

io.on('connection', (socket) => {
  // At this point, socket.user should be populated if authentication was successful
  if (!socket.user) {
    // This should ideally not happen if the middleware correctly rejects unauthenticated sockets.
    console.error(`Socket ${socket.id} connected without user object after auth middleware. Disconnecting.`);
    socket.disconnect(true);
    return;
  }

  console.log(`User ${socket.user.id} (socket ${socket.id}) connected via Socket.IO.`);
  userSockets.set(socket.id, socket.user.id); // Store mapping

  socket.on('disconnect', () => {
    console.log(`User ${socket.user.id} (socket ${socket.id}) disconnected from Socket.IO.`);
    userSockets.delete(socket.id); // Clean up mapping
  });

  // Example listener (can be removed or adapted)
  socket.on('clientMessage', (data) => {
    console.log(`Message from client ${socket.user.id} (socket ${socket.id}):`, data);
    // Example: Echo back to the sender
    // socket.emit('serverMessage', { message: 'Server acknowledges your message!', originalData: data });
    // Example: Broadcast to all (except sender perhaps)
    // socket.broadcast.emit('serverMessage', { sender: socket.user.id, message: data.message });
  });

  // TODO: Add more specific socket event handlers as per plan (join, send, etc.) in Step 4.4 and 4.5

  // Handle 'join' event for room management
  socket.on('join', (data, callback) => {
    const { room_id } = data;
    if (!room_id) {
      console.error(`User ${socket.user.id} (socket ${socket.id}) tried to join without room_id.`);
      if (callback) callback({ status: 'error', message: 'room_id is required.' });
      return;
    }

    // Sockets are automatically removed from rooms on disconnect.
    // No need to leave previous rooms unless explicitly required by logic (e.g., user can only be in one room at a time).
    // For chat, a user can be 'in' multiple rooms (subscribed to updates from multiple chats).
    socket.join(room_id);
    console.log(`User ${socket.user.id} (socket ${socket.id}) joined room: ${room_id}`);

    // Optional: Send a status message to the room (excluding the sender)
    // socket.to(room_id).emit('status', {
    //   message: `User ${socket.user.nickname || socket.user.id} has joined the chat.`,
    //   user_id: socket.user.id,
    //   type: 'join_room'
    // });

    if (callback) callback({ status: 'ok', message: `Successfully joined room: ${room_id}` });
  });

  // Handle 'send' event for sending messages
  socket.on('send', async (data, callback) => {
    const { room_id, message_type = 'text', content, image_url, is_burn = false, is_anonymous = false } = data;
    const sender_id = socket.user.id;

    if (!room_id) {
      if (callback) callback({ status: 'error', message: 'room_id is required.' });
      return;
    }
    if (message_type === 'text' && !content) {
      if (callback) callback({ status: 'error', message: 'Content is required for text messages.' });
      return;
    }
    if (message_type === 'image' && !image_url) {
      if (callback) callback({ status: 'error', message: 'image_url is required for image messages.' });
      return;
    }

    try {
      // 1. Persist message to database
      const chatMessage = await sequelize.models.ChatMessage.create({
        room_id,
        sender_id,
        message_type,
        content: message_type === 'text' ? content : null,
        image_url: message_type === 'image' ? image_url : null,
        is_burn,
        is_anonymous
      });

      // 2. Prepare message for broadcasting
      //    - For anonymous messages, do not reveal sender's actual ID to other clients.
      //    - Include database-generated fields like id and created_at.
      let messageToBroadcast = {
        id: chatMessage.id,
        room_id: chatMessage.room_id,
        message_type: chatMessage.message_type,
        content: chatMessage.content,
        image_url: chatMessage.image_url,
        is_burn: chatMessage.is_burn,
        is_anonymous: chatMessage.is_anonymous,
        created_at: chatMessage.created_at,
        // Sender information:
        // If anonymous, use a placeholder or generic sender info.
        // If not anonymous, include sender's actual details (e.g., id, nickname, avatar from socket.user or fetched).
        sender: is_anonymous
          ? { id: null, nickname: 'Anonymous', avatar_url: null } // Or some other placeholder
          : { id: socket.user.id, openid: socket.user.openid /* nickname/avatar can be added if available on socket.user */ }
      };

      // If not anonymous and more sender details are needed and not on socket.user, fetch them:
      // if (!is_anonymous && (!socket.user.nickname || !socket.user.avatar_url)) {
      //    const senderDetails = await User.findByPk(sender_id, { attributes: ['nickname', 'avatar_url'] });
      //    if (senderDetails) {
      //        messageToBroadcast.sender.nickname = senderDetails.nickname;
      //        messageToBroadcast.sender.avatar_url = senderDetails.avatar_url;
      //    }
      // }


      // 3. Broadcast the message to all clients in the room (including sender for confirmation)
      io.to(room_id).emit('receive', messageToBroadcast);

      console.log(`User ${sender_id} sent message to room ${room_id}:`, chatMessage.toJSON());
      if (callback) callback({ status: 'ok', message: 'Message sent and persisted.', messageId: chatMessage.id });

    } catch (error)
    {
      console.error(`Error saving or broadcasting message from user ${sender_id} to room ${room_id}:`, error);
      if (callback) callback({ status: 'error', message: 'Failed to send message.', error: error.message });
    }
  });
});

async function initializeDatabase() {
  try {
    await sequelize.authenticate();
    console.log('Database connection established successfully.');
    // Sequelize sync (optional, use with caution, especially in prod)
    if (process.env.NODE_ENV === 'development') {
      await sequelize.sync({ alter: true }); // alter: true tries to update schema without dropping data
      console.log("Development: All models were synchronized successfully via sequelize.sync().");
    }
  } catch (error) {
    console.error('Unable to connect to the database or sync models:', error);
    // Not exiting here to allow script to complete in this environment
  }
}

initializeDatabase();

module.exports = { app, server, io, sequelize };
