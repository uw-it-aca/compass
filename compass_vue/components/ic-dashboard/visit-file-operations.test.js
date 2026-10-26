import { flushPromises, mount } from "@vue/test-utils";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import VisitFileOperations from "./visit-file-operations.vue";

vi.mock("@/utils/data", () => ({
  uploadVisitFile: vi.fn(),
  getICVisitOptions: vi.fn(),
}));
vi.mock("bootstrap", () => ({ Modal: { getInstance: vi.fn() } }));

describe("visit file export", () => {
  let wrapper;
  let click;

  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-10-26T12:00:00Z"));
    vi.stubGlobal("fetch", vi.fn());
    vi.stubGlobal("URL", class extends URL {
      static createObjectURL = vi.fn(() => "blob:visits");
      static revokeObjectURL = vi.fn();
    });
    click = vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(() => {});
    wrapper = mount(VisitFileOperations);
    wrapper.vm.exportOptions = { start_date: "2026-10-01", end_date: "2026-10-26" };
  });

  afterEach(() => {
    wrapper.unmount();
    vi.runOnlyPendingTimers();
    vi.useRealTimers();
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("blocks duplicate requests and saves one complete CSV", async () => {
    let finish;
    fetch.mockReturnValue(new Promise((resolve) => { finish = resolve; }));
    const first = wrapper.vm.handleDownload();
    await wrapper.vm.handleDownload();
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(wrapper.vm.isDownloading).toBe(true);
    await wrapper.vm.$nextTick();
    expect(wrapper.get('button[type="submit"]').attributes("disabled")).toBeDefined();
    expect(click).not.toHaveBeenCalled();
    finish({
      ok: true,
      headers: new Headers({ "Content-Type": "text/csv" }),
      blob: async () => new Blob(["complete CSV"]),
    });
    await first;
    expect(fetch).toHaveBeenCalledWith(
      "/api/internal/visits/file/?start_date=2026-10-01&end_date=2026-10-26",
      expect.any(Object),
    );
    expect(click).toHaveBeenCalledTimes(1);
    expect(wrapper.vm.isDownloading).toBe(false);
    vi.runOnlyPendingTimers();
    expect(URL.revokeObjectURL).toHaveBeenCalledWith("blob:visits");
  });

  it("aborts a pending request on unmount without reporting an error", async () => {
    fetch.mockImplementation((url, { signal }) => new Promise((resolve, reject) => {
      signal.addEventListener("abort", () => reject(new DOMException("Aborted", "AbortError")));
    }));
    const instance = wrapper.vm;
    const download = instance.handleDownload();
    const signal = fetch.mock.calls[0][1].signal;
    wrapper.unmount();
    await download;
    expect(signal.aborted).toBe(true);
    expect(instance.downloadErrorResponse).toBeNull();
    expect(instance.isDownloading).toBe(false);
    expect(instance.exportAbortController).toBeNull();
    expect(click).not.toHaveBeenCalled();
  });

  it("ignores responses arriving after unmount even if fetch ignores abort", async () => {
    let finish;
    fetch.mockReturnValue(new Promise(resolve => { finish = resolve; }));
    const download = wrapper.vm.handleDownload();
    wrapper.unmount();
    const blob = vi.fn();
    finish({ ok: true, blob });
    await download;
    expect(blob).not.toHaveBeenCalled();
    expect(URL.createObjectURL).not.toHaveBeenCalled();
    expect(click).not.toHaveBeenCalled();
  });

  it("does not save an old response body after remounting", async () => {
    let finishBody;
    fetch.mockResolvedValueOnce({
      ok: true,
      headers: new Headers({ "Content-Type": "text/csv" }),
      blob: () => new Promise(resolve => { finishBody = resolve; }),
    });
    const oldDownload = wrapper.vm.handleDownload();
    await flushPromises();
    const oldSignal = fetch.mock.calls[0][1].signal;
    wrapper.unmount();
    wrapper = mount(VisitFileOperations);
    fetch.mockResolvedValueOnce({
      ok: true,
      headers: new Headers({ "Content-Type": "text/csv" }),
      blob: async () => new Blob(["new export"]),
    });
    await wrapper.vm.handleDownload();
    finishBody(new Blob(["old export"]));
    await oldDownload;
    expect(oldSignal.aborted).toBe(true);
    expect(fetch).toHaveBeenCalledTimes(2);
    expect(URL.createObjectURL).toHaveBeenCalledTimes(1);
    expect(click).toHaveBeenCalledTimes(1);
  });

  it("shows server errors without saving a file", async () => {
    fetch.mockResolvedValue({ ok: false, json: async () => "Select a smaller date range" });
    await wrapper.vm.handleDownload();
    await flushPromises();
    expect(wrapper.get('[role="alert"]').text()).toBe("Select a smaller date range");
    expect(click).not.toHaveBeenCalled();
    expect(wrapper.vm.isDownloading).toBe(false);
  });

  it.each([401, 403])("shows sign-in guidance for a plain-text HTTP %s response", async (status) => {
    fetch.mockResolvedValue(new Response("Invalid session", {
      status,
      headers: { "Content-Type": "text/plain" },
    }));
    await wrapper.vm.handleDownload();
    expect(wrapper.get('[role="alert"]').text()).toContain("Refresh the page and sign in again");
    expect(wrapper.vm.isDownloading).toBe(false);
    expect(wrapper.vm.exportAbortController).toBeNull();
    expect(click).not.toHaveBeenCalled();
  });

  it("does not save a partially transferred response", async () => {
    fetch.mockResolvedValue({
      ok: true,
      headers: new Headers({ "Content-Type": "text/csv" }),
      blob: async () => { throw new Error("Network transfer interrupted"); },
    });
    await wrapper.vm.handleDownload();
    expect(wrapper.vm.downloadErrorResponse).toBe("Network transfer interrupted");
    expect(click).not.toHaveBeenCalled();
    expect(wrapper.vm.isDownloading).toBe(false);
  });

  it("rejects reversed, missing, or excessive date ranges", async () => {
    for (const dates of [
      { start_date: "2026-10-26", end_date: "2026-10-01" },
      { start_date: "", end_date: "2026-10-26" },
      { start_date: "2025-01-01", end_date: "2026-10-26" },
    ]) {
      wrapper.vm.exportOptions = dates;
      await wrapper.vm.handleDownload();
      expect(wrapper.vm.downloadErrorResponse).toBeTruthy();
    }
    expect(fetch).not.toHaveBeenCalled();
  });

  it("allows any start date and bounds the end to an inclusive 366-day range", async () => {
    await wrapper.setData({
      exportOptions: { start_date: "2024-01-01", end_date: "2024-12-31" },
    });
    const start = wrapper.get("#visit-export-start");
    const end = wrapper.get("#visit-export-end");
    expect(start.attributes("min")).toBe("2008-01-01");
    expect(start.attributes("max")).toBeUndefined();
    expect(end.attributes("min")).toBe("2024-01-01");
    expect(end.attributes("max")).toBe("2024-12-31");
    expect(start.element.checkValidity()).toBe(true);
    expect(end.element.checkValidity()).toBe(true);

    await end.setValue("2025-01-01");
    expect(end.element.validity.rangeOverflow).toBe(true);

    await start.setValue("2024-01-02");
    expect(end.attributes("max")).toBe("2025-01-01");
    expect(start.element.checkValidity()).toBe(true);
    expect(end.element.checkValidity()).toBe(true);
  });

  it("adjusts the end date when navigating to an older or newer start year", async () => {
    const start = wrapper.get("#visit-export-start");
    const end = wrapper.get("#visit-export-end");
    await start.setValue("2024-01-01");
    expect(wrapper.vm.exportOptions.end_date).toBe("2024-12-31");
    expect(start.element.checkValidity()).toBe(true);
    expect(end.element.checkValidity()).toBe(true);

    await start.setValue("2027-02-01");
    expect(wrapper.vm.exportOptions.end_date).toBe("2027-02-01");
    expect(end.element.checkValidity()).toBe(true);
  });

  it("keeps an existing valid end date when the start changes", async () => {
    await wrapper.get("#visit-export-start").setValue("2026-09-01");
    expect(wrapper.vm.exportOptions.end_date).toBe("2026-10-26");
  });

  it("removes end-date bounds when the start is cleared", async () => {
    await wrapper.get("#visit-export-start").setValue("");
    expect(wrapper.get("#visit-export-end").attributes("max")).toBeUndefined();
    expect(wrapper.get("#visit-export-start").attributes("min")).toBe("2008-01-01");
    expect(wrapper.get("#visit-export-end").attributes("min")).toBe("2008-01-01");
  });

  it("starts the year selector at 2008 and rejects earlier exports", async () => {
    const years = wrapper.findAll("#visit-export-year option").map(option => option.text());
    expect(years.at(-1)).toBe("2008");
    expect(years).not.toContain("2007");
    await wrapper.get("#visit-export-start").setValue("2007-12-31");
    expect(wrapper.get("#visit-export-start").element.validity.rangeUnderflow).toBe(true);
    await wrapper.vm.handleDownload();
    expect(wrapper.vm.downloadErrorResponse).toContain("January 1, 2008");
    expect(fetch).not.toHaveBeenCalled();
  });

  it("allows a monthly export beginning January 1, 2008", async () => {
    fetch.mockResolvedValue({
      ok: true,
      headers: new Headers({ "Content-Type": "text/csv" }),
      blob: async () => new Blob(["header"]),
    });
    await wrapper.get("#visit-export-year").setValue(2008);
    await wrapper.get('[aria-label="Download January 2008"]').trigger("click");
    await flushPromises();
    expect(fetch).toHaveBeenCalledWith(
      "/api/internal/visits/file/?start_date=2008-01-01&end_date=2008-01-31",
      expect.any(Object),
    );
  });

  it("announces download progress and completion outside the busy region", async () => {
    let finish;
    fetch.mockReturnValue(new Promise(resolve => { finish = resolve; }));
    const download = wrapper.vm.handleDownload();
    await wrapper.vm.$nextTick();
    const status = wrapper.get("#visit-export-status");
    expect(status.attributes("role")).toBe("status");
    expect(status.attributes("aria-atomic")).toBe("true");
    expect(status.element.closest("[aria-busy]")).toBeNull();
    expect(status.text()).toBe("Preparing export...");
    finish({
      ok: true,
      headers: new Headers({ "Content-Type": "text/csv" }),
      blob: async () => new Blob(["header"]),
    });
    await download;
    expect(status.text()).toContain("CSV download requested in your browser");
  });

  it("announces automatic end-date adjustments but not unchanged dates", async () => {
    await wrapper.get("#visit-export-start").setValue("2024-01-01");
    expect(wrapper.get("#visit-export-status").text()).toContain("End date adjusted to December 31, 2024");
    await wrapper.get("#visit-export-start").setValue("2024-02-01");
    expect(wrapper.get("#visit-export-status").text()).toBe("");
  });

  it("names the import dialog and associates labels with each field", async () => {
    await wrapper.setData({
      isLoadingOptions: false,
      visitOptions: { program_areas: [], tutoring_options: [] },
    });
    expect(wrapper.get("#importDataModal").attributes("aria-labelledby")).toBe("visit-import-title");
    expect(wrapper.get("#visit-import-title").text()).toBe("Instructional Center Data Upload");
    for (const identifier of ["visit-import-program-area", "visit-import-tutoring-option", "visit-import-file", "checkin_date"]) {
      expect(wrapper.get(`#${identifier}`).element.labels[0].textContent).toBeTruthy();
    }
  });

  it("rejects login pages returned instead of CSV", async () => {
    fetch.mockResolvedValue({ ok: true, headers: new Headers({ "Content-Type": "text/html" }) });
    await wrapper.vm.handleDownload();
    expect(wrapper.vm.downloadErrorResponse).toContain("Refresh the page");
    expect(click).not.toHaveBeenCalled();
  });

  it("opens exports in a labeled modal with the custom range first", () => {
    expect(wrapper.get('[data-bs-target="#exportDataModal"]').text()).toBe("Export Data");
    expect(wrapper.get("#exportDataModal").attributes("aria-labelledby")).toBe("visit-export-title");
    expect(wrapper.get("#visit-export-title").text()).toBe("Export Visits");
    expect(wrapper.findAll("#exportDataModal h3").map(heading => heading.text())).toEqual([
      "Custom Date Range", "Monthly Export",
    ]);
  });

  it.each([
    [2024, "February", "2024-02-01", "2024-02-29"],
    [2025, "February", "2025-02-01", "2025-02-28"],
    [2025, "December", "2025-12-01", "2025-12-31"],
  ])("downloads %s %s with one month click", async (year, month, start, end) => {
    fetch.mockResolvedValue({
      ok: true,
      headers: new Headers({ "Content-Type": "text/csv" }),
      blob: async () => new Blob(["complete CSV"]),
    });
    await wrapper.get("#visit-export-year").setValue(year);
    await wrapper.get(`[aria-label="Download ${month} ${year}"]`).trigger("click");
    await flushPromises();
    expect(fetch).toHaveBeenCalledExactlyOnceWith(
      `/api/internal/visits/file/?start_date=${start}&end_date=${end}`,
      expect.any(Object),
    );
    expect(click).toHaveBeenCalledTimes(1);
    expect(click.mock.instances[0].download).toBe(`compass_visit_data_${start}_${end}.csv`);
    expect(wrapper.vm.exportOptions).toEqual({ start_date: "2026-10-01", end_date: "2026-10-26" });
  });

  it("disables future months in the current year", async () => {
    expect(wrapper.get('[aria-label="Download October 2026"]').attributes("disabled")).toBeUndefined();
    expect(wrapper.get('[aria-label="Download November 2026"]').attributes("disabled")).toBeDefined();
    expect(wrapper.get('[aria-label="Download December 2026"]').attributes("disabled")).toBeDefined();
    await wrapper.vm.handleMonthDownload(10);
    expect(fetch).not.toHaveBeenCalled();
    await wrapper.get("#visit-export-year").setValue(2025);
    expect(wrapper.get('[aria-label="Download December 2025"]').attributes("disabled")).toBeUndefined();
  });

  it("locks all export controls while a month is downloading", async () => {
    let finish;
    fetch.mockReturnValue(new Promise(resolve => { finish = resolve; }));
    const download = wrapper.vm.handleMonthDownload(8);
    await wrapper.vm.$nextTick();
    expect(wrapper.get('[aria-label="Download September 2026"] .spinner-border').exists()).toBe(true);
    for (const control of wrapper.findAll("#exportDataModal input, #exportDataModal select, #exportDataModal button:not(.btn-close)")) {
      expect(control.attributes("disabled")).toBeDefined();
    }
    await wrapper.vm.handleDownload();
    await wrapper.vm.handleMonthDownload(7);
    expect(fetch).toHaveBeenCalledTimes(1);
    finish({ ok: false, json: async () => "Try a smaller range" });
    await download;
    expect(wrapper.vm.activeExport).toBeNull();
    expect(wrapper.get("#exportDataModal [role='alert']").text()).toBe("Try a smaller range");
  });
});
