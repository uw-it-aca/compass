import path from "node:path";
import { fileURLToPath } from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
export const targets = {
  compass: { origin: "https://test.compass.uw.edu", entry: "/caseload" },
};

export function getTarget(name = "compass") {
  if (!Object.hasOwn(targets, name)) {
    throw new Error("This suite targets Compass test only.");
  }
  return {
    ...targets[name],
    statePath: path.join(directory, ".auth", `${name}.json`),
  };
}

export function isTargetResponse(response, target, pathnamePattern) {
  const url = new URL(response.url());
  return url.origin === target.origin &&
    response.request().method() === "GET" &&
    pathnamePattern.test(url.pathname);
}
