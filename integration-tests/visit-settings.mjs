import { readFileSync } from "node:fs";

export function validateVisitSettings(settings) {
  const netid = settings?.visitStudentNetid;
  if (typeof netid !== "string" || !/^[a-z][a-z0-9]{1,31}$/.test(netid)) {
    throw new Error("Configure a valid visitStudentNetid in ignored local-settings.json.");
  }
  return { netid };
}

export function loadVisitSettings() {
  let settings;
  try {
    settings = JSON.parse(readFileSync(new URL("./local-settings.json", import.meta.url), "utf8"));
  } catch {
    throw new Error("Create ignored local-settings.json with visitStudentNetid before running visit tests.");
  }
  return validateVisitSettings(settings);
}