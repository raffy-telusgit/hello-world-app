// Flat ESLint config (ESLint v9). Type-aware-lite setup: JS + TypeScript
// recommended rules, with Prettier turned off-conflicting rules last.
const js = require("@eslint/js");
const tseslint = require("typescript-eslint");
const prettier = require("eslint-config-prettier");

module.exports = tseslint.config(
  // Only lint application source; skip build output and config files.
  { ignores: ["dist/**", "node_modules/**", "eslint.config.js"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ["src/**/*.ts"],
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: "module",
    },
    rules: {
      // Allow intentionally-unused args/vars when prefixed with `_`.
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
    },
  },
  // Keep last: disables stylistic rules that would fight Prettier.
  prettier,
);
