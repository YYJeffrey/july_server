const express = require('express');
const eventController = require('../controllers/eventController');
const { authenticateToken } = require('../middlewares/authMiddleware');

const router = express.Router();

// POST /api/events - Create a new event
router.post('/', authenticateToken, eventController.createEvent);

// GET /api/events - Get a list of events (Placeholder)
router.get('/', eventController.getEvents);

// GET /api/events/:id - Get event details (Placeholder)
router.get('/:id', eventController.getEventById);

// POST /api/events/:id/join - Join an event (Placeholder)
router.post('/:id/join', authenticateToken, eventController.joinEvent);

// DELETE /api/events/:id/leave - Leave an event (Placeholder)
router.delete('/:id/leave', authenticateToken, eventController.leaveEvent);

// GET /api/events/:id/participants - Get event participants (Placeholder)
router.get('/:id/participants', eventController.getEventParticipants);

// PUT /api/events/:id - Update an event (Placeholder, requires auth and possibly ownership check)
router.put('/:id', authenticateToken, eventController.updateEvent);

// DELETE /api/events/:id - Delete an event (Placeholder, requires auth and possibly ownership check)
router.delete('/:id', authenticateToken, eventController.deleteEvent);


module.exports = router;
