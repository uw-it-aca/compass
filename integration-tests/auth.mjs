import { mkdir, chmod } from "node:fs/promises";
import path from "node:path";
import { createInterface } from "node:readline/promises";
import { chromium } from "@playwright/test";
import { getTarget } from "./targets.mjs";

process.umask(0o077);
const target = getTarget(process.argv[2]);
const browser = await chromium.launch({ headless: false });
const prompt = createInterface({ input: process.stdin, output: process.stdout });

try {
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto(new URL(target.entry, target.origin).href);
  await prompt.question(
    "Complete normal SAML/MFA login in the browser. Once the app is ready, press Enter here. ",
  );
  if (new URL(page.url()).origin !== target.origin) {
    throw new Error("Login did not return to the expected test application. State not saved.");
  }
  const cookies = await context.cookies(target.origin);
  if (!cookies.some((cookie) => cookie.httpOnly)) {
    throw new Error("No HTTP-only application cookie found. State not saved.");
  }
  await mkdir(path.dirname(target.statePath), { recursive: true, mode: 0o700 });
  await chmod(path.dirname(target.statePath), 0o700);
  await context.storageState({ path: target.statePath });
  await chmod(target.statePath, 0o600);
  console.log("Saved local session. Run the smoke test to verify application access.");
} finally {
  prompt.close();
  await browser.close();
}
