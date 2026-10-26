export function activeVisits(payload) {
  if (!Array.isArray(payload?.pending_verification) ||
      !payload.by_programarea || typeof payload.by_programarea !== "object" ||
      !Object.values(payload.by_programarea).every(Array.isArray)) {
    throw new Error("Active visit response has an unexpected structure.");
  }
  return [...payload.pending_verification, ...Object.values(payload.by_programarea).flat()];
}

export function chooseVisitOptions(options) {
  const areas = options.program_areas || [];
  const writingArea = areas.find((area) => String(area.slug).includes("writing"));
  const area = areas.find((candidate) =>
    (candidate === writingArea ? options.writing_services : options.courses)?.length,
  );
  const tutoring = options.tutoring_options?.[0];
  const service = (area === writingArea ? options.writing_services : options.courses)?.[0];
  if (!area || !tutoring || !service) {
    throw new Error("Visit prerequisite unavailable: no usable program, tutoring, and course/service combination.");
  }
  return { area: String(area.slug), tutoring: String(tutoring.slug), service: String(service.id) };
}