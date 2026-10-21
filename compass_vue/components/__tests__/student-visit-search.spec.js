import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";

vi.mock("@/utils/data", () => ({
  getStudentBySearch: vi.fn(),
  getStudentDetail: vi.fn(),
  getStudentVisits: vi.fn(),
  getStudentEligibility: vi.fn(),
  getEligibilities: vi.fn(),
  setStudentEligibility: vi.fn(),
  getICVisitOptions: vi.fn(),
  createICVisit: vi.fn(),
}));
vi.mock("@/directives/lazyload", () => ({ default: {} }));

import { createICVisit } from "@/utils/data";
import StudentVisitSearch from "@/components/ic-dashboard/student-visit-search.vue";

const visitOptions = {
  program_areas: [
    { id: 27, name: "IC Drop-In Tutoring", slug: "ic-drop-in-tutoring" },
  ],
  tutoring_options: [{ id: 2, name: "Workshop", slug: "workshop" }],
  writing_services: [{ id: 1, name: "Application" }],
  courses: [{ id: "G H 401", name: "G H 401" }],
};

function mountInCheckinMode() {
  window.icVisitsEligibilitySlug = "ic";
  return mount(StudentVisitSearch, {
    global: { stubs: { studenvisitsummary: true } },
    data() {
      return {
        searchValue: "javerage",
        person: { system_key: "002367923", student: {} },
        studentEligibility: [{ slug: "ic" }],
        creatingCheckin: true,
        isLoadingOptions: false,
        visitOptions,
      };
    },
  });
}

describe("StudentVisitSearch check-in", () => {
  beforeEach(() => {
    createICVisit.mockReset();
    createICVisit.mockResolvedValue({});
  });

  it("sends program area and tutoring option slugs", async () => {
    const wrapper = mountInCheckinMode();
    const selects = wrapper.findAll("select");

    await selects[0].setValue("ic-drop-in-tutoring");
    await selects[1].setValue("workshop");
    await selects[2].setValue("G H 401");
    await wrapper
      .findAll("button")
      .find((b) => b.text() === "Create Check In")
      .trigger("click");
    await flushPromises();

    expect(createICVisit).toHaveBeenCalledWith({
      student_syskey: "002367923",
      program_area: "ic-drop-in-tutoring",
      tutoring_option: "workshop",
      course: "G H 401",
      writing_service: null,
    });
  });
});
