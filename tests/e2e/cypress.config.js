const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: process.env.BASE_URL || 'http://localhost:8081',
    supportFile: false,
    video: false,
    screenshotOnRunFailure: false,
  },
});
