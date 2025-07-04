'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class EventParticipant extends Model {
    static associate(models) {
      EventParticipant.belongsTo(models.Event, {
        foreignKey: 'event_id',
        as: 'event',
        onDelete: 'CASCADE',
      });
      EventParticipant.belongsTo(models.User, {
        foreignKey: 'user_id',
        as: 'user',
        onDelete: 'CASCADE',
      });
    }
  }
  EventParticipant.init({
    id: {
      allowNull: false,
      autoIncrement: true,
      primaryKey: true,
      type: DataTypes.INTEGER
    },
    event_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'events',
        key: 'id',
      },
      onUpdate: 'CASCADE',
      onDelete: 'CASCADE',
    },
    user_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'users',
        key: 'id',
      },
      onUpdate: 'CASCADE',
      onDelete: 'CASCADE',
    },
    joined_at: {
      allowNull: false,
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW
    }
  }, {
    sequelize,
    modelName: 'EventParticipant',
    tableName: 'event_participants',
    timestamps: true, // Keep Sequelize's default timestamps
    createdAt: 'joined_at', // Map createdAt to joined_at
    updatedAt: false, // Participation records usually don't update their own fields
    indexes: [
      {
        unique: true,
        fields: ['event_id', 'user_id'] // Unique constraint for a user per event
      }
    ]
  });
  return EventParticipant;
};
