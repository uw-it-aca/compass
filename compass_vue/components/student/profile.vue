<template>
  <div class="bg-gray rounded-3">
    <div class="row">
      <div class="col-xl-6 mb-3">
        <div class="d-flex p-3">
          <div class="pe-3">
            <div class="rounded-circle border border-4" :style="profileStyles">
              &nbsp;
            </div>
          </div>
          <div class="flex-fill">
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
              <span class="ms-2">({{ person.pronouns }})</span>
            </div>
            <div class="h5">
              {{ person.student.student_number }},
              {{ person.uwnetid }}
            </div>
            <ul>
              <li>Full name: {{ person.full_name }}</li>
              <li>
                First and last: {{ person.first_name }} {{ person.surname }}
              </li>
              <li>DOB: {{ person.student.birthdate }}</li>
              <li>Ethnicity: {{ person.student.assigned_ethnic_desc }}</li>
              <li>Disability: {{ person.student.disability_ind }}</li>
              <li>
                Veterans: {{ person.student.veteran_benefit_code }},
                {{ person.student.veteran_benefit_desc }},
                {{ person.student.veteran_desc }}
              </li>
            </ul>
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
      </div>
      <div class="col-12 col-xl-3 mb-3">
        <div class="p-3">
          <ul class="list-unstyled m-0">
            <li>Citizenship: {{ person.student.citizen_country }}</li>
            <li>
              Visa Type:
              <span v-if="person.student.visa_type">
                {{ person.student.visa_type }}
              </span>
              <span v-else> N/A </span>
            </li>
            <li>Resident status: {{ person.student.resident_desc }}</li>
          </ul>
        </div>
      </div>
      <div class="col-12 col-xl-3">
        <div class="p-3">
          <ul class="list-unstyled m-0">
            <li>UW Email: {{ person.student.student_email }}</li>
            <li>Personal email: {{ person.student.personal_email }}</li>
            <li>Local Phone: {{ person.student.local_phone_number }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import dataMixin from "../../mixins/data_mixin.js";
export default {
  mixins: [dataMixin],
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {},
  data() {
    return {
      photo: null,
    };
  },
  computed: {
    profileStyles() {
      console.log({
        background: "url('" + this.photo + "') no-repeat center",
        // else... use url '/static/compass/img/photo.jpg'
        "background-size": "cover",
        width: "120px",
        height: "120px",
      });
      return {
        background: "url('" + this.photo + "') no-repeat center",
        // else... use url '/static/compass/img/photo.jpg'
        "background-size": "cover",
        width: "120px",
        height: "120px",
      };
    },
    personPhotoUrl() {
      return this.person.photo_url
        ? this.person.photo_url
        : "/static/compass/img/photo.jpg";
    },
  },
  created: function () {
    var _this = this;
    this.getStudentPhoto(this.person.photo_url).then((photo) => {
      _this.photo = photo.data;
    });
  },
};
</script>
