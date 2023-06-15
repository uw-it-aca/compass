import dayjs from "dayjs";
import localizedFormat from "dayjs/plugin/localizedFormat";
dayjs.extend(localizedFormat);

function formatDate(date, format) {
  if (!date) {
    return null;
  }
  return dayjs(date).format(format);
}

function getToday() {
  let today = dayjs();
  return today;
}

function getYesterday() {
  let today = dayjs();
  let yesterday = today.subtract("1", "day");
  return yesterday;
}

function getWeeksApart(quarterStartDate, compareDate) {
  const days = dayjs(compareDate).diff(
    dayjs(quarterStartDate).startOf("week"),
    "days"
  );
  if (days < 0) {
    return 0;
  } else {
    return parseInt(days / 7) + 1;
  }
}

function getMinutesApart(startDate, endDate) {
    return dayjs(endDate).diff(startDate, 'minutes')
}

export { formatDate, getToday, getYesterday, getWeeksApart, getMinutesApart };
