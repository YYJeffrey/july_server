const { Event, User } = require('../models'); // User might be needed for organizer details later
const { sequelize } = require('../models'); // For transactions if needed

// Validation helper (basic example)
function validateEventInput(data) {
  const errors = [];
  if (!data.title || data.title.trim() === '') {
    errors.push('Title is required.');
  }
  if (!data.event_time) {
    errors.push('Event time is required.');
  } else if (isNaN(new Date(data.event_time).getTime())) {
    errors.push('Invalid event time format.');
  }
  if (!data.location_type || !['online', 'offline'].includes(data.location_type)) {
    errors.push('Location type must be "online" or "offline".');
  }
  if (data.location_type === 'offline' && (!data.location_detail || data.location_detail.trim() === '')) {
    errors.push('Location detail is required for offline events.');
  }
   if (data.location_type === 'online' && (!data.location_detail || data.location_detail.trim() === '')) {
    errors.push('Location detail (e.g., meeting URL) is required for online events.');
  }
  if (data.max_participants !== undefined && (typeof data.max_participants !== 'number' || data.max_participants < 0)) {
    errors.push('Max participants must be a non-negative number.');
  }
  if (data.duration_minutes !== undefined && (typeof data.duration_minutes !== 'number' || data.duration_minutes <= 0)) {
    errors.push('Duration must be a positive number of minutes.');
  }
  // Add more validations as needed (e.g., title length, description length, cover_image_url format)
  return errors;
}


/**
 * POST /events - Create a new event
 */
async function createEvent(req, res) {
  const organizer_id = req.user.id; // From authenticateToken middleware
  const eventData = req.body;

  const validationErrors = validateEventInput(eventData);
  if (validationErrors.length > 0) {
    return res.status(400).json({ message: 'Validation failed.', errors: validationErrors });
  }

  try {
    const newEvent = await Event.create({
      ...eventData,
      organizer_id,
      status: eventData.status || 'draft', // Default to draft if not provided, or validate allowed initial statuses
      participants_count: 0, // Initialize participants count
    });

    return res.status(201).json(newEvent);

  } catch (error) {
    console.error('Error creating event:', error);
    if (error.name === 'SequelizeValidationError' || error.name === 'SequelizeUniqueConstraintError') {
      return res.status(400).json({ message: 'Validation error creating event.', errors: error.errors.map(e => e.message) });
    }
    return res.status(500).json({ message: 'Failed to create event.', error: error.message });
  }
}

// Placeholder for other event controller functions
async function getEvents(req, res) {
  const { page = 1, limit = 10, status, organizer_id, sort_by = 'event_time', order = 'ASC' } = req.query;
  const offset = (parseInt(page, 10) - 1) * parseInt(limit, 10);

  const whereClause = {};
  if (status) {
    // Ensure status is one of the allowed enum values if necessary, or handle potential SQL injection if status is free text.
    // For now, assuming status is a valid value from the ENUM.
    whereClause.status = status;
  }
  if (organizer_id) {
    whereClause.organizer_id = parseInt(organizer_id, 10);
  }

  // Validate sort_by to prevent arbitrary column sorting leading to errors or info disclosure
  const allowedSortBy = ['event_time', 'created_at', 'title', 'participants_count'];
  const sortField = allowedSortBy.includes(sort_by) ? sort_by : 'event_time';
  const sortOrder = ['ASC', 'DESC'].includes(order.toUpperCase()) ? order.toUpperCase() : 'ASC';

  try {
    const { count, rows } = await Event.findAndCountAll({
      where: whereClause,
      include: [
        {
          model: User,
          as: 'organizer',
          attributes: ['id', 'nickname', 'avatar_url'], // Select only necessary fields
        },
        // Optionally, include participant count directly if not relying solely on `participants_count` field
        // or if you want to show some participant details in the list.
      ],
      limit: parseInt(limit, 10),
      offset: offset,
      order: [[sortField, sortOrder]],
      distinct: true, // Important for count when using include with hasMany
    });

    return res.status(200).json({
      totalPages: Math.ceil(count / limit),
      currentPage: parseInt(page, 10),
      totalEvents: count,
      events: rows,
    });

  } catch (error) {
    console.error('Error fetching events:', error);
    return res.status(500).json({ message: 'Failed to fetch events.', error: error.message });
  }
}
async function getEventById(req, res) {
  const { id } = req.params;

  try {
    const event = await Event.findByPk(id, {
      include: [
        {
          model: User,
          as: 'organizer',
          attributes: ['id', 'nickname', 'avatar_url'],
        },
        // We could also include participants here if needed, but there's a separate endpoint for them.
        // For example, to get a count or a few preview participants:
        // {
        //   model: models.EventParticipant,
        //   as: 'participants',
        //   attributes: ['user_id'], // Or include User model for participant details
        //   limit: 5 // Preview a few participants
        // }
      ],
    });

    if (!event) {
      return res.status(404).json({ message: 'Event not found.' });
    }

    // Note: `event.participants_count` is the denormalized count.
    // If we wanted to show actual participant details, the /events/:id/participants endpoint is better.
    return res.status(200).json(event);

  } catch (error) {
    console.error(`Error fetching event ${id}:`, error);
    return res.status(500).json({ message: 'Failed to fetch event details.', error: error.message });
  }
}
async function joinEvent(req, res) {
  const { id: eventId } = req.params;
  const userId = req.user.id;

  try {
    const result = await sequelize.transaction(async (t) => {
      const event = await Event.findByPk(eventId, { transaction: t });

      if (!event) {
        // This will cause the transaction to rollback
        return { status: 404, message: 'Event not found.' };
      }

      // Check event status (e.g., only allow joining 'upcoming' events)
      if (event.status !== 'upcoming') {
        return { status: 400, message: `Cannot join event with status: ${event.status}. Only 'upcoming' events can be joined.` };
      }

      // Check if event is full
      if (event.max_participants > 0 && event.participants_count >= event.max_participants) {
        return { status: 400, message: 'Event is already full.' };
      }

      // Check if user has already joined
      const existingParticipant = await sequelize.models.EventParticipant.findOne({
        where: { event_id: eventId, user_id: userId },
        transaction: t,
      });

      if (existingParticipant) {
        return { status: 409, message: 'You have already joined this event.' }; // 409 Conflict
      }

      // Create participation record
      await sequelize.models.EventParticipant.create({
        event_id: eventId,
        user_id: userId,
      }, { transaction: t });

      // Increment participants_count
      await event.increment('participants_count', { by: 1, transaction: t });

      return { status: 200, message: 'Successfully joined the event.', event }; // Return event or some confirmation
    });

    // If result has a status, it means a controlled "error" or condition was met
    if (result.status !== 200) {
        return res.status(result.status).json({ message: result.message });
    }

    return res.status(200).json({ message: result.message });

  } catch (error) {
    console.error(`Error joining event ${eventId} for user ${userId}:`, error);
    // Handle potential race conditions or other DB errors if not caught by transaction logic
    if (error.name === 'SequelizeUniqueConstraintError') { // Should be caught by findOne check, but as a fallback
        return res.status(409).json({ message: 'You have already joined this event.' });
    }
    return res.status(500).json({ message: 'Failed to join event.', error: error.message });
  }
}
async function leaveEvent(req, res) {
  const { id: eventId } = req.params;
  const userId = req.user.id;

  try {
    const result = await sequelize.transaction(async (t) => {
      const event = await Event.findByPk(eventId, { transaction: t });
      if (!event) {
        return { status: 404, message: 'Event not found.' };
      }

      // Optional: Check event status (e.g., can only leave 'upcoming' events)
      // if (event.status !== 'upcoming') {
      //   return { status: 400, message: `Cannot leave event with status: ${event.status}.` };
      // }

      const participantRecord = await sequelize.models.EventParticipant.findOne({
        where: { event_id: eventId, user_id: userId },
        transaction: t,
      });

      if (!participantRecord) {
        return { status: 404, message: 'You are not currently a participant of this event.' };
      }

      // Delete participation record
      await participantRecord.destroy({ transaction: t });

      // Decrement participants_count, ensuring it doesn't go below zero
      if (event.participants_count > 0) {
        await event.decrement('participants_count', { by: 1, transaction: t });
      } else {
        // This case should ideally not happen if counts are managed correctly
        console.warn(`Event ${eventId} participants_count was already 0 or less when user ${userId} tried to leave.`);
        // Optionally, set to 0 if it somehow became negative, though decrement handles this.
        // await event.update({ participants_count: 0 }, { transaction: t });
      }

      return { status: 200, message: 'Successfully left the event.' };
    });

    if (result.status !== 200) {
        return res.status(result.status).json({ message: result.message });
    }
    return res.status(200).json({ message: result.message });

  } catch (error) {
    console.error(`Error leaving event ${eventId} for user ${userId}:`, error);
    return res.status(500).json({ message: 'Failed to leave event.', error: error.message });
  }
}
async function getEventParticipants(req, res) {
  const { id: eventId } = req.params;
  // Optional: Add pagination if lists can be very long
  // const { page = 1, limit = 30 } = req.query;
  // const offset = (parseInt(page, 10) - 1) * parseInt(limit, 10);

  try {
    const event = await Event.findByPk(eventId);
    if (!event) {
      return res.status(404).json({ message: 'Event not found.' });
    }

    // Fetch participants and include their User model details
    const participants = await sequelize.models.EventParticipant.findAll({
      where: { event_id: eventId },
      include: [
        {
          model: User,
          as: 'user',
          attributes: ['id', 'nickname', 'avatar_url'], // Specify attributes to return for privacy
        },
      ],
      order: [['joined_at', 'ASC']], // Show who joined first
      // limit: parseInt(limit, 10),
      // offset: offset,
    });

    // Extract just the user details from the participant records
    const participantUsers = participants.map(p => p.user);

    return res.status(200).json(participantUsers);

  } catch (error) {
    console.error(`Error fetching participants for event ${eventId}:`, error);
    return res.status(500).json({ message: 'Failed to fetch event participants.', error: error.message });
  }
}
async function updateEvent(req, res) {
  const { id: eventId } = req.params;
  const userId = req.user.id; // Authenticated user
  const eventData = req.body;

  // Basic validation for updatable fields (similar to createEvent but for partial updates)
  // For simplicity, we'll allow updating title, description, event_time, location, etc.
  // More granular validation can be added.
  // IMPORTANT: Some fields like organizer_id, participants_count should not be updatable directly via this endpoint.

  const validationErrors = []; // validateEventInput(eventData, true /* isUpdate = true */); // Adapt validation
  if (eventData.title !== undefined && eventData.title.trim() === '') {
    validationErrors.push('Title cannot be empty.');
  }
  if (eventData.event_time && isNaN(new Date(eventData.event_time).getTime())) {
    validationErrors.push('Invalid event time format.');
  }
  if (eventData.location_type && !['online', 'offline'].includes(eventData.location_type)) {
    validationErrors.push('Location type must be "online" or "offline".');
  }
  // Add more specific field validations as needed.

  if (validationErrors.length > 0) {
    return res.status(400).json({ message: 'Validation failed.', errors: validationErrors });
  }

  try {
    const event = await Event.findByPk(eventId);

    if (!event) {
      return res.status(404).json({ message: 'Event not found.' });
    }

    // Authorization: Only organizer can update the event
    if (event.organizer_id !== userId) {
      return res.status(403).json({ message: 'Forbidden: You are not the organizer of this event.' });
    }

    // Prevent updating status to certain values directly, or if event has participants, etc.
    // For example, can't change a 'completed' event details easily.
    // if (event.status === 'completed' || event.status === 'cancelled') {
    //   return res.status(400).json({ message: `Cannot update event with status: ${event.status}.` });
    // }

    // Define updatable fields
    const allowedUpdates = [
        'title', 'description', 'event_time',
        'location_type', 'location_detail', 'max_participants',
        'duration_minutes', 'cover_image_url', 'status' // Be cautious with status updates
    ];
    const updatesToApply = {};
    for (const key of allowedUpdates) {
        if (eventData.hasOwnProperty(key)) {
            updatesToApply[key] = eventData[key];
        }
    }

    if (Object.keys(updatesToApply).length === 0) {
        return res.status(400).json({ message: 'No valid fields provided for update.' });
    }

    await event.update(updatesToApply);
    return res.status(200).json(event);

  } catch (error) {
    console.error(`Error updating event ${eventId}:`, error);
    if (error.name === 'SequelizeValidationError') {
      return res.status(400).json({ message: 'Validation error updating event.', errors: error.errors.map(e => e.message) });
    }
    return res.status(500).json({ message: 'Failed to update event.', error: error.message });
  }
}
async function deleteEvent(req, res) {
  const { id: eventId } = req.params;
  const userId = req.user.id; // Authenticated user

  try {
    const event = await Event.findByPk(eventId);

    if (!event) {
      return res.status(404).json({ message: 'Event not found.' });
    }

    // Authorization: Only organizer can delete (cancel) the event
    if (event.organizer_id !== userId) {
      return res.status(403).json({ message: 'Forbidden: You are not the organizer of this event.' });
    }

    // Instead of hard delete, change status to 'cancelled'
    // Or, if event is in 'draft', perhaps allow hard delete.
    if (event.status === 'completed' || event.status === 'cancelled') {
      return res.status(400).json({ message: `Event is already ${event.status} and cannot be cancelled again.` });
    }

    // For a 'draft' event, one might choose to destroy it:
    // if (event.status === 'draft') {
    //   await event.destroy();
    //   return res.status(204).send(); // No content
    // }

    // For other statuses, change to 'cancelled'
    event.status = 'cancelled';
    await event.save();

    // Note: If an event is cancelled, you might want to notify participants.
    // This logic would typically be handled by an event listener or a service method.

    return res.status(200).json({ message: 'Event has been cancelled successfully.', event });

  } catch (error) {
    console.error(`Error cancelling event ${eventId}:`, error);
    return res.status(500).json({ message: 'Failed to cancel event.', error: error.message });
  }
}


module.exports = {
  createEvent,
  getEvents,
  getEventById,
  joinEvent,
  leaveEvent,
  getEventParticipants,
  updateEvent,
  deleteEvent,
};
