// web/eslint.config.js
export default [
  {
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'script',
      globals: { window: 'readonly', document: 'readonly' },
    },
    rules: {
      semi: 'warn',
      'no-unused-vars': 'warn',
      'no-console': 'off',
    },
  },
];
