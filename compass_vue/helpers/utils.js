import dayjs from "dayjs";

function formatDate(dateString) {
  const date = dayjs(dateString);
  return date.format("MMMM D, YYYY");
}

function getToday() {
  let today = dayjs();
  return today.format("MMMM D, YYYY");
}

function getYesterday() {
  let today = dayjs();
  let tomorrow = today.subtract("1", "day");
  return tomorrow.format("MMMM D, YYYY");
}

function getUserRole() {
  // mock a user role for dev and testing
  return { role: "Super" };
}

export { formatDate, getToday, getYesterday, getUserRole };
