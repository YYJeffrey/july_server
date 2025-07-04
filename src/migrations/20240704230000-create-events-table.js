'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('events', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      organizer_id: {
        type: Sequelize.INTEGER,
        allowNull: false,
        references: {
          model: 'users', // Name of the target table
          key: 'id',
        },
        onUpdate: 'CASCADE',
        onDelete: 'CASCADE', // If an organizer is deleted, their events are also deleted.
      },
      title: {
        type: Sequelize.STRING,
        allowNull: false
      },
      description: {
        type: Sequelize.TEXT,
        allowNull: true
      },
      event_time: {
        type: Sequelize.DATE, // DATETIME
        allowNull: false
      },
      location_type: {
        type: Sequelize.ENUM('online', 'offline'),
        allowNull: false
      },
      location_detail: {
        type: Sequelize.STRING, // E.g. URL for 'online', address for 'offline'
        allowNull: true
      },
      max_participants: {
        type: Sequelize.INTEGER,
        allowNull: false,
        defaultValue: 0 // 0 for unlimited
      },
      participants_count: {
        type: Sequelize.INTEGER,
        allowNull: false,
        defaultValue: 0
      },
      duration_minutes: {
        type: Sequelize.INTEGER,
        allowNull: true
      },
      cover_image_url: {
        type: Sequelize.STRING,
        allowNull: true
      },
      status: {
        type: Sequelize.ENUM('draft', 'upcoming', 'ongoing', 'completed', 'cancelled'),
        allowNull: false,
        defaultValue: 'draft'
      },
      created_at: {
        allowNull: false,
        type: Sequelize.DATE,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      },
      updated_at: {
        allowNull: false,
        type: Sequelize.DATE,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
      }
    });

    // Add indexes
    await queryInterface.addIndex('events', ['organizer_id']);
    await queryInterface.addIndex('events', ['event_time']);
    await queryInterface.addIndex('events', ['status']);
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('events');
  }
};
