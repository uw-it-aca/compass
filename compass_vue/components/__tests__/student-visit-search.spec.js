import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import localOptionsJson from "../../../compass/resources/compass_visits/file/api/v1/visitoptions/9136CCB8F66711D5BE060004AC494FFE?raw";

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
    { id: 28, name: "Writing Assistance", slug: "ic-writing-assistance" },
  ],
  tutoring_options: [{ id: 2, name: "Workshop", slug: "workshop" }],
  writing_services: [{ id: 1, name: "Application" }],
  courses: [{ id: "G H 401", name: "G H 401" }],
};

function mountInCheckinMode(options = visitOptions) {
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
        visitOptions: options,
      };
    },
  });
}

describe("StudentVisitSearch check-in", () => {
  beforeEach(() => {
    createICVisit.mockReset();
    createICVisit.mockResolvedValue({});
  });

  it.each([
    ["ic-writing-assistance", 1, null, 1],
    ["ic-drop-in-tutoring", "ENGL 131", "ENGL 131", null],
  ])("supports local mock options for %s", async (programArea, selection, course, writingService) => {
    const localOptions = JSON.parse(localOptionsJson);
    const wrapper = mountInCheckinMode(localOptions);
    const selects = wrapper.findAll("select");

    await selects[0].setValue(programArea);
    await selects[1].setValue("individual");
    await selects[2].setValue(selection);
    await wrapper.findAll("button").find(
      (button) => button.text() === "Create Check In",
    ).trigger("click");
    await flushPromises();

    expect(createICVisit).toHaveBeenCalledWith({
      student_syskey: "002367923",
      program_area: programArea,
      tutoring_option: "individual",
      course,
      writing_service: writingService,
    });
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

  it("shows only writing services for the writing program area", async () => {
    const wrapper = mountInCheckinMode();
    const selects = wrapper.findAll("select");

    await selects[0].setValue("ic-writing-assistance");

    expect(selects[2].find('optgroup[label="Writing Services"]').exists()).toBe(true);
    expect(selects[2].find('optgroup[label="Courses"]').exists()).toBe(false);
    expect(selects[2].text()).toContain("Application");
    expect(selects[2].text()).not.toContain("G H 401");
  });

  it("shows only courses for other program areas", async () => {
    const wrapper = mountInCheckinMode();
    const selects = wrapper.findAll("select");

    await selects[0].setValue("ic-drop-in-tutoring");

    expect(selects[2].find('optgroup[label="Courses"]').exists()).toBe(true);
    expect(selects[2].find('optgroup[label="Writing Services"]').exists()).toBe(false);
    expect(selects[2].text()).toContain("G H 401");
    expect(selects[2].text()).not.toContain("Application");
  });

  it.each([
    ["ic-drop-in-tutoring", "G H 401", "ic-writing-assistance"],
    ["ic-writing-assistance", 1, "ic-drop-in-tutoring"],
  ])("clears the selection when switching from %s", async (initialArea, selection, nextArea) => {
    const wrapper = mountInCheckinMode();
    const selects = wrapper.findAll("select");
    const createButton = wrapper.findAll("button").find(
      (button) => button.text() === "Create Check In",
    );

    await selects[0].setValue(initialArea);
    await selects[1].setValue("workshop");
    await selects[2].setValue(selection);
    expect(createButton.element.disabled).toBe(false);

    await selects[0].setValue(nextArea);

    expect(wrapper.vm.checkInData.courseOrWritingService).toBe("");
    expect(createButton.element.disabled).toBe(true);
  });

  it.each([
    ["ic-writing-assistance", null, 1],
    ["ic-drop-in-tutoring", 1, null],
  ])("submits only the matching option type for %s", async (programArea, course, writingService) => {
    const wrapper = mountInCheckinMode({
      ...visitOptions,
      courses: [{ id: 1, name: "G H 401" }],
    });
    const selects = wrapper.findAll("select");

    await selects[0].setValue(programArea);
    await selects[1].setValue("workshop");
    await selects[2].setValue(1);
    await wrapper.findAll("button").find(
      (button) => button.text() === "Create Check In",
    ).trigger("click");
    await flushPromises();

    expect(createICVisit).toHaveBeenCalledWith({
      student_syskey: "002367923",
      program_area: programArea,
      tutoring_option: "workshop",
      course,
      writing_service: writingService,
    });
  });
});
