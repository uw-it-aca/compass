import assert from "node:assert/strict";
import { test } from "node:test";
import { validateVisitSettings } from "../visit-settings.mjs";

test("visit settings require a configured identifier without leaking invalid values", () => {
  assert.deepEqual(validateVisitSettings({ visitStudentNetid: "synthetic1" }), { netid: "synthetic1" });
  for (const settings of [null, {}, { visitStudentNetid: "invalid value" }]) {
    assert.throws(() => validateVisitSettings(settings), /Configure a valid visitStudentNetid/);
  }
});