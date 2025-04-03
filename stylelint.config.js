/** @type {import('stylelint').Config} */
export default {
  extends: [
    "stylelint-config-standard-scss",
    "stylelint-config-standard-vue/scss",
  ],
  customSyntax: "postcss-html",
  overrides: [
    {
      files: ["*.vue", "**/*.vue"],
      rules: {
        "scss/no-global-function-names": null,
        "no-invalid-position-at-import-rule": null,
        "scss/at-import-partial-extension": [
          "never",
          {
            severity: "warning",
          },
        ],
      },
    },
  ],
};
