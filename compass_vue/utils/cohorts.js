import { getToday } from "@/utils/dates.js";

function getCohorts(n) {
  let thisYear = getToday().year(),
    cohorts = [];

  for (let i = 0; i < n; i++) {
    cohorts.push({
      start_year: thisYear,
      end_year: thisYear + 1,
    });

    thisYear -= 1;
  }

  return cohorts;
}

export { getCohorts };
