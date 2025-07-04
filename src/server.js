const { server } = require('./app');
const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
  console.log(`Ginco MiniApp Server is listening on port ${PORT}`);
  console.log(`Access API at http://localhost:${PORT}/api/health`);
  if (process.env.NODE_ENV === 'development') {
    console.log("Server running in Development mode.");
  } else if (process.env.NODE_ENV === 'production') {
    console.log("Server running in Production mode.");
  } else {
    console.log(`Server running in mode: ${process.env.NODE_ENV || 'not set (defaults to development effectively for some libs)'}`);
  }
});
