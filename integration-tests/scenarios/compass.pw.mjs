import { test, expect } from "@playwright/test";
import { getTarget, isTargetResponse } from "../targets.mjs";

test("authenticated caseload renders a live response", async ({ page }) => {
  const target = getTarget("compass");
  const responsePromise = page.waitForResponse(
    (response) => isTargetResponse(
      response, target, /^\/api\/internal\/adviser\/[^/]+\/caseload\/$/,
    ),
  );
  await page.goto(target.entry);
  const response = await responsePromise;
  expect(response.status(), "Caseload API must succeed").toBe(200);
  expect(response.headers()["content-type"]?.includes("application/json")).toBe(true);
  const payload = await response.json();
  expect(Array.isArray(payload.caseload), "An empty caseload is valid").toBe(true);
  await expect(page.getByRole("heading", { name: "Caseload", exact: true })).toBeVisible();
  await expect(page.locator("#classFilter")).toBeVisible();
});
