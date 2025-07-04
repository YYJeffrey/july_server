'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('chat_messages', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.BIGINT
      },
      room_id: {
        type: Sequelize.STRING,
        allowNull: false,
      },
      sender_id: {
        type: Sequelize.INTEGER,
        allowNull: false,
        references: {
          model: 'users', // Name of the target table
          key: 'id',
        },
        onUpdate: 'CASCADE',
        onDelete: 'CASCADE', // Consider implications: if user is deleted, their messages are deleted.
                           // Alternative: SET NULL (if sender_id allows NULL) or RESTRICT.
      },
      message_type: {
        type: Sequelize.ENUM('text', 'image'),
        allowNull: false,
        defaultValue: 'text'
      },
      content: {
        type: Sequelize.TEXT,
        allowNull: true
      },
      image_url: {
        type: Sequelize.STRING,
        allowNull: true
      },
      is_burn: {
        type: Sequelize.BOOLEAN,
        allowNull: false,
        defaultValue: false
      },
      is_anonymous: {
        type: Sequelize.BOOLEAN,
        allowNull: false,
        defaultValue: false
      },
      created_at: {
        allowNull: false,
        type: Sequelize.DATE,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      }
      // No `updated_at` column as per model's `updatedAt: false`
    });

    // Add indexes for frequently queried columns
    await queryInterface.addIndex('chat_messages', ['room_id']);
    await queryInterface.addIndex('chat_messages', ['sender_id']);
    await queryInterface.addIndex('chat_messages', ['created_at']);
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('chat_messages');
  }
};
