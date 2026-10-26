import { defineConfig } from "@playwright/test";
import { getTarget, targets } from "./targets.mjs";

export default defineConfig({
  testDir: "./scenarios",
  testMatch: "**/*.pw.mjs",
  workers: 1,
  retries: 0,
  timeout: 60_000,
  expect: { timeout: 15_000 },
  reporter: [["line"]],
  use: {
    browserName: "chromium",
    navigationTimeout: 45_000,
    actionTimeout: 15_000,
    trace: "off",
    screenshot: "off",
    video: "off",
  },
  projects: Object.keys(targets).map((name) => ({
    name,
    testMatch: `**/${name}.pw.mjs`,
    use: {
      baseURL: getTarget(name).origin,
      storageState: getTarget(name).statePath,
    },
  })),
});
