import { test, expect } from "@playwright/test";
import { getTarget } from "../targets.mjs";
import { loadVisitSettings } from "../visit-settings.mjs";
import { activeVisits, chooseVisitOptions } from "../visit-data.mjs";

const activePath = "/api/internal/visits/active_visits/";

test("staff searches, creates an active visit, and checks it out", async ({ page }) => {
  test.setTimeout(180_000);
  const { netid } = loadVisitSettings();
  const target = getTarget();
  let createdId;
  let checkedOut = false;
  let studentSyskey;

  function waitForAPI(pathname, method = "GET") {
    return page.waitForResponse((response) => {
      const url = new URL(response.url());
      return url.origin === target.origin && url.pathname === pathname &&
        response.request().method() === method;
    }, { timeout: 30_000 });
  }

  async function jsonResponse(response) {
    expect(response.status(), "Workflow API must succeed").toBe(200);
    expect(response.headers()["content-type"]?.includes("application/json")).toBe(true);
    return response.json();
  }

  async function currentActiveVisits() {
    const response = await page.request.get(new URL(activePath, target.origin).href);
    return activeVisits(await jsonResponse(response));
  }

  function studentRow() {
    return page.getByRole("row").filter({
      has: page.getByRole("link", { name: netid, exact: true }),
    });
  }

  try {
    const initialActive = waitForAPI(activePath);
    await page.goto("/ic-dashboard");
    await expect(page.getByRole("heading", { name: "Instructional Center Dashboard", exact: true }).first()).toBeVisible();
    const initialVisits = activeVisits(await jsonResponse(await initialActive));
    expect(initialVisits.some((visit) => visit.student?.uwnetid === netid),
      "Prerequisite: configured student must have no active or pending visit").toBe(false);

    await page.getByRole("textbox", { name: "Student number or UW netid", exact: true }).fill(netid);
    const studentResponse = waitForAPI(`/api/internal/student/${netid}/`);
    await page.getByRole("button", { name: "Search", exact: true }).click();
    const student = await jsonResponse(await studentResponse);
    expect(student.uwnetid === netid, "Search must resolve the configured identity").toBe(true);
    studentSyskey = String(student.system_key);
    expect(Boolean(student.system_key && student.uwregid), "Student prerequisites must be available").toBe(true);
    expect(initialVisits.some((visit) => String(visit.student_syskey) === studentSyskey),
      "Prerequisite: configured student must have no open visit").toBe(false);

    const modal = page.locator("#studentSearchModal");
    await expect(modal.getByText("IC Eligible", { exact: true })).toBeVisible();
    const optionsResponse = waitForAPI(`/api/internal/visit_options/${student.uwregid}/`);
    await modal.getByRole("button", { name: "Check In", exact: true }).click();
    const choices = chooseVisitOptions(await jsonResponse(await optionsResponse));
    const selects = modal.getByRole("combobox");
    await expect(selects).toHaveCount(3);
    await selects.nth(0).selectOption(choices.area);
    await selects.nth(1).selectOption(choices.tutoring);
    await selects.nth(2).selectOption(choices.service);

    expect((await currentActiveVisits()).some((visit) => String(visit.student_syskey) === studentSyskey),
      "Prerequisite changed: student acquired an open visit").toBe(false);
    const createResponse = waitForAPI("/api/internal/visits/create/", "POST");
    const refreshedActive = waitForAPI(activePath);
    await modal.getByRole("button", { name: "Create Check In", exact: true }).click();
    const created = await jsonResponse(await createResponse);
    expect(Number.isInteger(Number(created.id)) && Number(created.id) > 0, "Creation must return a visit ID").toBe(true);
    createdId = Number(created.id);
    expect(String(created.student_syskey) === studentSyskey, "Created visit must belong to configured student").toBe(true);
    const active = activeVisits(await jsonResponse(await refreshedActive));
    expect(active.some((visit) => Number(visit.id) === createdId), "Created visit must appear in active API list").toBe(true);

    await modal.getByRole("button", { name: "Close", exact: true }).click();
    await expect(modal).toBeHidden();
    await expect(studentRow()).toHaveCount(1);
    if (!active.find((visit) => Number(visit.id) === createdId).is_verified) {
      const verifyResponse = waitForAPI(`/api/internal/visits/update/${createdId}/`, "PATCH");
      const verifiedActiveResponse = waitForAPI(activePath);
      await studentRow().getByRole("button", { name: "Verify", exact: true }).click();
      const verified = await jsonResponse(await verifyResponse);
      expect(Number(verified.id) === createdId && verified.is_verified === true,
        "Verification must update only this run's visit").toBe(true);
      await jsonResponse(await verifiedActiveResponse);
    }
    await expect(studentRow().getByRole("button", { name: "Check Out", exact: true })).toBeVisible();
    const ownedVisits = (await currentActiveVisits()).filter((visit) => String(visit.student_syskey) === studentSyskey);
    expect(ownedVisits.length === 1 && Number(ownedVisits[0].id) === createdId,
      "Checkout must target only this run's visit").toBe(true);

    const checkoutResponse = waitForAPI(`/api/internal/visits/update/${createdId}/`, "PATCH");
    const afterCheckoutResponse = waitForAPI(activePath);
    await studentRow().getByRole("button", { name: "Check Out", exact: true }).click();
    const checkout = await jsonResponse(await checkoutResponse);
    expect(Number(checkout.id) === createdId, "Checkout must return the created visit").toBe(true);
    expect(Boolean(checkout.check_out_date), "Checkout must persist a timestamp").toBe(true);
    checkedOut = true;
    const remaining = activeVisits(await jsonResponse(await afterCheckoutResponse));
    expect(remaining.some((visit) => Number(visit.id) === createdId), "Checked-out visit must leave active API list").toBe(false);
    await expect(studentRow()).toHaveCount(0);
  } finally {
    if (createdId && !checkedOut) {
      try {
        const remaining = (await currentActiveVisits()).find((visit) => Number(visit.id) === createdId);
        if (remaining) {
          expect(String(remaining.student_syskey) === studentSyskey,
            "Cleanup must match the created visit's student").toBe(true);
          const headers = {
          "X-CSRFToken": await page.locator('[name="csrfmiddlewaretoken"]').first().inputValue(),
          "X-Requested-With": "XMLHttpRequest",
          "Referer": new URL("/ic-dashboard", target.origin).href,
          };
          const url = new URL(`/api/internal/visits/update/${createdId}/`, target.origin).href;
          if (!remaining.is_verified) {
            const verified = await page.request.patch(url, { data: { is_verified: true }, headers });
            expect(verified.ok(), "Cleanup verification must succeed").toBe(true);
          }
          const response = await page.request.patch(url, { data: { is_checked_out: true }, headers });
          expect(response.ok(), "Cleanup checkout must succeed").toBe(true);
          expect((await currentActiveVisits()).some((visit) => Number(visit.id) === createdId),
            "Cleanup must remove this run's visit from the active list").toBe(false);
        }
      } catch {
        console.warn("Cleanup failed: this run's visit may remain active; review before rerunning.");
      }
    }
  }
});