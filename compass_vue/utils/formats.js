function formatPhoneNumber(phoneNumber) {
  var phoneNumberString = Math.floor(parseFloat(phoneNumber)).toString();
  var cleaned = ("" + phoneNumberString).replace(/\D/g, "");
  var match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
  if (match) {
    return "(" + match[1] + ") " + match[2] + "-" + match[3];
  }
  return null;
}

function formatAdviserName(person) {
  return (person.preferred_first_name && person.preferred_surname)
    ? person.preferred_first_name + " " + person.preferred_surname
    : person.display_name;
}

export { formatPhoneNumber, formatAdviserName };
