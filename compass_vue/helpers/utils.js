import dayjs from 'dayjs';

function formatDate(dateString) {
  const date = dayjs(dateString);
  return date.format('MMMM D, YYYY');
}

function getToday() {
  let today = dayjs();
  return today.format('MMMM D, YYYY');
}

function getTomorrow() {
  let today = dayjs();
  let tomorrow = today.add('1', 'day');
  return tomorrow.format('MMMM D, YYYY');
}

export { formatDate, getToday, getTomorrow };
