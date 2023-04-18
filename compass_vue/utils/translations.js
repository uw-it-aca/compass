function translateTrueFalse(value) {
  return value ? "Yes" : "No";
}

function translateMilitaryTime(time) {
  var hours = parseInt(time.substr(0, 2));
  var minutes = time.substr(3, 2);
  var suffix = hours >= 12 ? "PM" : "AM";
  hours = hours % 12;
  hours = hours ? hours : 12;
  return hours + ":" + minutes + " " + suffix;
}

export { translateTrueFalse, translateMilitaryTime };
