'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class User extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
      // Example:
      // User.hasMany(models.Post, { foreignKey: 'userId', as: 'posts' });
    }
  }
  User.init({
    id: {
      allowNull: false,
      autoIncrement: true,
      primaryKey: true,
      type: DataTypes.INTEGER
    },
    openid: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true
    },
    session_key: {
      type: DataTypes.STRING,
      allowNull: false
      // Note: Consider encrypting this at rest if security policies require it.
      // Sequelize doesn't do this automatically. Application-level encryption would be needed.
    },
    nickname: {
      type: DataTypes.STRING,
      allowNull: true
    },
    avatar_url: {
      type: DataTypes.STRING,
      allowNull: true
    },
    gender: {
      type: DataTypes.INTEGER,
      allowNull: true // 0: unknown, 1: male, 2: female
    },
    country: {
      type: DataTypes.STRING,
      allowNull: true
    },
    province: {
      type: DataTypes.STRING,
      allowNull: true
    },
    city: {
      type: DataTypes.STRING,
      allowNull: true
    },
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
    modelName: 'User',
    tableName: 'users', // Explicitly define table name
    timestamps: true, // Enable Sequelize's default timestamp handling
    createdAt: 'created_at', // Map Sequelize's createdAt to our column name
    updatedAt: 'updated_at'  // Map Sequelize's updatedAt to our column name
  });
  return User;
};
