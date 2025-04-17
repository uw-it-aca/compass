import dayjs from "dayjs";
import localizedFormat from "dayjs/plugin/localizedFormat";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";
import relativeTime from "dayjs/plugin/relativeTime";

dayjs.extend(localizedFormat);
dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(relativeTime);

const LOCAL_TIMEZONE = "America/Los_Angeles";

function formatDate(date, format) {
  return date ? dayjs(date).format(format) : null;
}

function formatUTCToLocalDate(date, format) {
  return formatDate(utcToLocalDate(date), format);
}

function formatUTCToLocalDateAndTimeZone(date, format) {
  let local_date = utcToLocalDate(date);

  return formatDate(local_date, format) + nonLocalTimeZone(local_date);
}

function utcToLocalDate(date) {
  return date ? dayjs(date).tz(LOCAL_TIMEZONE) : null;
}

function nonLocalTimeZone(local_date) {
  return dayjs.tz.guess() == LOCAL_TIMEZONE
    ? ""
    : Math.abs(local_date.utcOffset()) == 420
      ? " PDT"
      : " PST";
}

function utcDate(date) {
  return dayjs(date).tz(dayjs.tz.utc);
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
  return dayjs(endDate).diff(startDate, "minutes");
}

function getTimeFromNow(date) {
  return dayjs().to(dayjs(date));
  //return dayjs().fromNow(date);
}

export {
  formatDate,
  formatUTCToLocalDate,
  formatUTCToLocalDateAndTimeZone,
  getToday,
  getYesterday,
  getWeeksApart,
  getMinutesApart,
  getTimeFromNow,
};
