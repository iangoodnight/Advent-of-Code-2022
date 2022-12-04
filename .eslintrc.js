/** @format */

module.exports = {
  env: {
    commonjs: true,
    es2021: true,
    node: true,
  },
  extends: ['airbnb', 'prettier'],
  parserOptions: {
    ecmaVersion: 12,
  },
  plugins: ['prettier'],
  rules: {
    'linebreak-style': ['error', 'unix'],
    'no-console': 'off',
    'prettier/prettier': ['error'],
    quotes: ['error', 'single'],
    semi: ['error', 'always'],
  },
};
