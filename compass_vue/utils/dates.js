import dayjs from "dayjs";
import localizedFormat from "dayjs/plugin/localizedFormat";
dayjs.extend(localizedFormat);

function formatDate(date, format) {
  if (!date) {
    return null;
  }
  return dayjs(date).format(format);
}

export { formatDate };
