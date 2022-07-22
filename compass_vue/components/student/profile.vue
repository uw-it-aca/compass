<template>
  <div class="bg-gray p-3 rounded-3">
    <div class="row">
      <div class="col-lg-4 pe-4 d-flex small">
        <div>
          <div class="rounded-circle border border-4" style="width: 140px">
            <img
              :src="person.photo_url"
              class="img-fluid rounded-circle border border-white border-2"
            />
          </div>
        </div>
        <div class="flex-fill ps-4 mb-4">
          <div class="h3 text-dark axdd-font-encode-sans">
            <template v-if="person.preferred_first_name">
              {{ person.preferred_first_name }}
            </template>
            <template v-else> {{ person.first_name }} </template>&nbsp;
            <template v-if="person.preferred_surname">
              {{ person.preferred_surname }}
            </template>
            <template v-else>
              {{ person.surname }}
            </template>
          </div>
          <div class="h5">
            {{ person.student.student_number }},
            <small>{{ person.uwnetid }}</small>
          </div>
          <p>
            <span
              class="badge rounded-pill border border-muted text-dark me-1"
              >{{ person.gender }}</span
            >
            <span class="badge rounded-pill border border-muted text-dark">
              {{ person.pronouns }}
            </span>
          </p>
          <div v-if="person.student.sports.length > 0">
            <i class="bi bi-trophy-fill text-purple"></i> Sport:
            <span
              v-for="(sport, index) in person.student.sports"
              :key="sport.code"
            >
              {{ sport.sport_code }}
              <span v-if="index + 1 < person.student.sports.length">, </span>
            </span>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-4 px-4 small">
        <ul class="list-unstyled m-0">
          <li>
            Preferred name: {{ person.preferred_first_name }}
            {{ person.preferred_middle_name }}
            {{ person.preferred_last_name }}
          </li>
          <li>Ethnicity: {{ person.student.assigned_ethnic_desc }}</li>
          <li>Citizenship: {{ person.student.resident_desc }}</li>
          <li>
            Visa Type:
            <span v-if="person.student.visa_type">
              {{ person.student.visa_type }}
            </span>
            <span v-else> N/A </span>
          </li>
          <li>DOB: {{ person.student.birthdate }}</li>
        </ul>
      </div>
      <div class="col-6 col-lg-4 ps-4 small">
        <ul class="list-unstyled m-0">
          <li>UW Email: {{ person.student.student_email }}</li>
          <li>Personal email: {{ person.student.personal_email }}</li>
          <li>Local Phone: {{ person.student.local_phone_number }}</li>
          <li class="mt-2">
            Perm Address:<br />
            {{ person.student.perm_addr_line1 }},
            {{ person.student.perm_addr_line2 }},
            {{ person.student.perm_addr_city }},
            {{ person.student.perm_addr_state }}
            {{ person.student.perm_addr_5digit_zip }},
            {{ person.student.perm_addr_country }}
          </li>
          <li class="mt-2">
            Local Address:<br />
            {{ person.student.local_addr_line1 }},
            {{ person.student.local_addr_line2 }},
            {{ person.student.local_addr_city }},
            {{ person.student.local_addr_state }}
            {{ person.student.local_addr_5digit_zip }},
            {{ person.student.local_addr_country }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {},
  data() {
    return {};
  },
};
</script>
