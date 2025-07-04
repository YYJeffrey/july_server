require('dotenv').config();

module.exports = {
  development: {
    username: process.env.DB_USERNAME || 'root',
    password: process.env.DB_PASSWORD || null,
    database: process.env.DB_DATABASE || 'database_dev',
    host: process.env.DB_HOST || '127.0.0.1',
    dialect: 'mysql',
    logging: console.log, // console.log or false
  },
  test: {
    username: process.env.DB_USERNAME_TEST || 'root',
    password: process.env.DB_PASSWORD_TEST || null,
    database: process.env.DB_DATABASE_TEST || 'database_test',
    host: process.env.DB_HOST_TEST || '127.0.0.1',
    dialect: 'mysql',
    logging: false,
  },
  production: {
    username: process.env.DB_USERNAME_PROD,
    password: process.env.DB_PASSWORD_PROD,
    database: process.env.DB_DATABASE_PROD,
    host: process.env.DB_HOST_PROD,
    dialect: 'mysql',
    logging: false,
  }
};
