'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('users', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      openid: {
        type: Sequelize.STRING,
        allowNull: false,
        unique: true
      },
      session_key: {
        type: Sequelize.STRING,
        allowNull: false
        // Sensitive data: ensure proper security measures are in place if storing directly.
        // Consider application-level encryption or a separate secure store if feasible.
      },
      nickname: {
        type: Sequelize.STRING,
        allowNull: true
      },
      avatar_url: {
        type: Sequelize.STRING,
        allowNull: true
      },
      gender: {
        type: Sequelize.INTEGER, // e.g., 0 for unknown, 1 for male, 2 for female
        allowNull: true
      },
      country: {
        type: Sequelize.STRING,
        allowNull: true
      },
      province: {
        type: Sequelize.STRING,
        allowNull: true
      },
      city: {
        type: Sequelize.STRING,
        allowNull: true
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
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('users');
  }
};
