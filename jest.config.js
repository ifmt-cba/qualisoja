module.exports = {
  testEnvironment: 'jsdom',
  testMatch: ['**/tests/**/*.test.js'],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  setupFilesAfterEnv: ['./tests/js/setup.js'],
  collectCoverage: true,
  collectCoverageFrom: [
    'templates/static/geral/js/**/*.js',
  ],
  coverageReporters: ['text', 'lcov'],
  testTimeout: 10000,
  verbose: true,
};
