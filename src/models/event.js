'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class Event extends Model {
    static associate(models) {
      Event.belongsTo(models.User, {
        foreignKey: 'organizer_id',
        as: 'organizer',
        onDelete: 'CASCADE', // Or RESTRICT/SET NULL based on policy if an organizer is deleted
      });
      Event.hasMany(models.EventParticipant, {
        foreignKey: 'event_id',
        as: 'participants', // This will be an array of EventParticipant records
        onDelete: 'CASCADE', // If an event is deleted, participant records are also deleted
      });
    }
  }
  Event.init({
    id: {
      allowNull: false,
      autoIncrement: true,
      primaryKey: true,
      type: DataTypes.INTEGER
    },
    organizer_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'users',
        key: 'id',
      },
      onUpdate: 'CASCADE',
      onDelete: 'CASCADE',
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false
    },
    description: {
      type: DataTypes.TEXT,
      allowNull: true
    },
    event_time: {
      type: DataTypes.DATE, // DATETIME
      allowNull: false
    },
    location_type: {
      type: DataTypes.ENUM('online', 'offline'),
      allowNull: false
    },
    location_detail: {
      type: DataTypes.STRING,
      allowNull: true
    },
    max_participants: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0 // 0 means unlimited
    },
    participants_count: { // This will be denormalized; needs careful updates
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0
    },
    duration_minutes: {
      type: DataTypes.INTEGER,
      allowNull: true
    },
    cover_image_url: {
      type: DataTypes.STRING,
      allowNull: true
    },
    status: {
      type: DataTypes.ENUM('draft', 'upcoming', 'ongoing', 'completed', 'cancelled'),
      allowNull: false,
      defaultValue: 'draft'
    },
    // Timestamps are handled by Sequelize by default if not specified otherwise
    created_at: {
      allowNull: false,
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW
    },
    updated_at: {
      allowNull: false,
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW
    }
  }, {
    sequelize,
    modelName: 'Event',
    tableName: 'events',
    timestamps: true, // Explicitly use Sequelize's timestamp handling
    createdAt: 'created_at',
    updatedAt: 'updated_at',
  });
  return Event;
};
