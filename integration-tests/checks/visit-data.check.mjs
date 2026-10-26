import assert from "node:assert/strict";
import { test } from "node:test";
import { activeVisits, chooseVisitOptions } from "../visit-data.mjs";

test("active visits include pending and verified groups without accepting malformed data", () => {
  assert.deepEqual(activeVisits({ pending_verification: [{ id: 1 }], by_programarea: { science: [{ id: 2 }] } }).map((visit) => visit.id), [1, 2]);
  assert.throws(() => activeVisits({}));
  assert.throws(() => activeVisits({ pending_verification: [], by_programarea: { science: null } }));
});

test("selects live available course or writing options", () => {
  const options = {
    program_areas: [{ slug: "science" }, { slug: "writing" }],
    tutoring_options: [{ slug: "individual" }],
    courses: [{ id: 12 }],
    writing_services: [{ id: 24 }],
  };
  assert.deepEqual(chooseVisitOptions(options), { area: "science", tutoring: "individual", service: "12" });
  assert.deepEqual(chooseVisitOptions({ ...options, courses: [] }), { area: "writing", tutoring: "individual", service: "24" });
  assert.throws(() => chooseVisitOptions({ ...options, courses: [], writing_services: [] }), /prerequisite unavailable/);
});