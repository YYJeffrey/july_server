'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class ChatMessage extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // Define association to User model (sender)
      ChatMessage.belongsTo(models.User, {
        foreignKey: 'sender_id',
        as: 'sender', // شناسه فرستنده
        onDelete: 'CASCADE', // If a user is deleted, their messages might also be deleted or anonymized depending on policy
      });
      // Note: No direct association for room_id as it's a dynamic string.
      // Room-based retrieval will be done via querying on room_id.
    }
  }
  ChatMessage.init({
    id: {
      allowNull: false,
      autoIncrement: true,
      primaryKey: true,
      type: DataTypes.BIGINT // As per plan
    },
    room_id: {
      type: DataTypes.STRING, // Can be user1id_user2id or group_uuid
      allowNull: false,
      // Index will be added in the migration
    },
    sender_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'users', // Name of the target table (usually plural)
        key: 'id',
      },
      onUpdate: 'CASCADE',
      onDelete: 'CASCADE', // Or SET NULL / RESTRICT depending on desired behavior
    },
    message_type: {
      type: DataTypes.ENUM('text', 'image'),
      allowNull: false,
      defaultValue: 'text'
    },
    content: { // For text messages
      type: DataTypes.TEXT,
      allowNull: true
    },
    image_url: { // For image messages
      type: DataTypes.STRING,
      allowNull: true
    },
    is_burn: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false
    },
    is_anonymous: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false
    },
    created_at: {
      allowNull: false,
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW
      // Index will be added in the migration
    }
    // Sequelize automatically handles `updatedAt` if timestamps: true (default)
    // but we only defined created_at in the plan.
    // If only created_at is needed, set `timestamps: true, updatedAt: false` in model options.
    // For chat messages, usually only creation time matters.
  }, {
    sequelize,
    modelName: 'ChatMessage',
    tableName: 'chat_messages',
    timestamps: true, // Enable Sequelize's default timestamp handling
    createdAt: 'created_at',
    updatedAt: false, // Chat messages are typically immutable after creation in terms of content
                      // Though flags like is_read might be updated, they'd be in separate tables or columns.
                      // For this schema, disabling updatedAt.
  });
  return ChatMessage;
};
