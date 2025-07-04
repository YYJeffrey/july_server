'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('event_participants', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      event_id: {
        type: Sequelize.INTEGER,
        allowNull: false,
        references: {
          model: 'events', // Name of the target table
          key: 'id',
        },
        onUpdate: 'CASCADE',
        onDelete: 'CASCADE', // If event is deleted, participation records are removed
      },
      user_id: {
        type: Sequelize.INTEGER,
        allowNull: false,
        references: {
          model: 'users', // Name of the target table
          key: 'id',
        },
        onUpdate: 'CASCADE',
        onDelete: 'CASCADE', // If user is deleted, their participation records are removed
      },
      joined_at: {
        allowNull: false,
        type: Sequelize.DATE,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      }
      // No `updated_at` as per model definition
    });

    // Add unique constraint for (event_id, user_id)
    await queryInterface.addConstraint('event_participants', {
      fields: ['event_id', 'user_id'],
      type: 'unique',
      name: 'event_participants_event_id_user_id_unique'
    });

    // Add indexes for foreign keys for performance
    await queryInterface.addIndex('event_participants', ['event_id']);
    await queryInterface.addIndex('event_participants', ['user_id']);
  },

  async down(queryInterface, Sequelize) {
    // It's good practice to remove constraints/indexes before dropping table, though dropTable often handles it.
    // await queryInterface.removeConstraint('event_participants', 'event_participants_event_id_user_id_unique');
    // await queryInterface.removeIndex('event_participants', ['event_id']);
    // await queryInterface.removeIndex('event_participants', ['user_id']);
    await queryInterface.dropTable('event_participants');
  }
};
