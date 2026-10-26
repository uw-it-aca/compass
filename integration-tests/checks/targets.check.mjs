import assert from "node:assert/strict";
import { test } from "node:test";
import { getTarget, isTargetResponse } from "../targets.mjs";

test("only deployed Compass test is a target", () => {
  assert.equal(getTarget().origin, "https://test.compass.uw.edu");
  assert.throws(() => getTarget("visits"));
  assert.throws(() => getTarget("production"));
  assert.throws(() => getTarget("toString"));
});

test("response matching rejects other origins and writes", () => {
  const response = (origin, method) => ({
    url: () => `${origin}/api/internal/profile/`,
    request: () => ({ method: () => method }),
  });
  const target = getTarget();
  const pattern = /^\/api\/internal\/profile\/$/;
  assert.equal(isTargetResponse(response(target.origin, "GET"), target, pattern), true);
  assert.equal(isTargetResponse(response("https://compass.uw.edu", "GET"), target, pattern), false);
  assert.equal(isTargetResponse(response(target.origin, "POST"), target, pattern), false);
});
