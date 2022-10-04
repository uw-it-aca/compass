<template>
  <div class="bg-gray rounded-3">
    <div class="row">
      <div class="col-xl-3 mb-3">
        <div class="p-3 text-center">
          <div class="d-inline-block rounded-circle border border-4 mb-2">
            <img
              :src="person.photo_url"
              @error="$event.target.src = '/static/compass/img/placeholder.png'"
              class="img-profile rounded-circle border bg-light border-white border-2"
            />
          </div>
          <!-- moved preferred name to under the profile photo -->
          <div class="h3 text-dark-beige axdd-font-encode-sans">
            <span class="me-1">
              <template v-if="person.preferred_first_name">
                {{ person.preferred_first_name }}
              </template>
              <template v-else>{{ person.first_name }}</template>
            </span>

            <span>
              <template v-if="person.preferred_surname">
                {{ person.preferred_surname }}
              </template>
              <template v-else>
                {{ person.surname }}
              </template>
            </span>
          </div>
          <!-- moved pronouns to under the preferred name -->
          <div class="h3 text-dark axdd-font-encode-sans">
            <template v-if="person.pronouns">
              {{ person.pronouns }}
            </template>
            <template v-else>he/him</template>
          </div>
          <div class="">
            {{ person.student.student_number }},
            {{ person.student.student_email }}
          </div>
        </div>
      </div>
      <div class="col-xl-3">
        <div class="p-3">
          <div class="body-1 flex-fill">
            <div class="fw-bold text-dark-beige mb-2">Personal Information</div>
            <ul class="list-unstyled m-0">
              <li><b>Full name: </b>{{ person.full_name }}</li>
              <li><b>First: </b>{{ person.first_name }}</li>
              <li><b>Last: </b>{{ person.surname }}</li>
              <li><b>Gender: </b>{{ person.student.gender }}</li>
              <li v-if="mq.xs" aria-hidden="true"><hr /></li>
              <li><b>DOB: </b>{{ person.student.birthdate }}</li>
              <li>
                <b>Ethnicity: </b>{{ person.student.assigned_ethnic_desc }}
              </li>
              <li>
                <b>Disability: </b>
                <span v-if="person.student.disability_ind"> Disabled </span>
                <span v-else> Not Disabled </span>
              </li>
              <li>
                <b>Veterans: </b>
                <span v-if="person.student.veteran_benefit_code === '0'">
                  Not A Vet
                </span>
                <span v-else>
                  {{ person.student.veteran_benefit_code }},
                  {{ person.student.veteran_benefit_desc }},
                  {{ person.student.veteran_desc }}
                </span>
              </li>
              <li>
                <strong>Phone:</strong> +1
                {{ person.student.local_phone_number }}
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
          <p class="text-dark-beige fs-6">
            <b>Immigration Status</b>
          </p>
          <ul class="list-unstyled m-0">
            <li><b>Citizenship: </b> {{ person.student.citizen_country }}</li>
            <li>
              <b>Visa Type: </b>
              <span v-if="person.student.visa_type">
                {{ person.student.visa_type }}
              </span>
              <span v-else> N/A </span>
            </li>
            <li><b>Residency: </b>{{ person.student.resident_desc }}</li>
          </ul>
        </div>
      </div>
      <div class="body-1 col-12 col-xl-3">
        <div class="p-3">
          <p class="text-dark-beige fs-6">
            <b>Address</b>
          </p>
          <ul class="list-unstyled m-0">
            <li>
              <b>Local Address: </b>
              <address>
                {{ person.student.local_addr_line1 }}
                {{ person.student.local_addr_line2 }},
                {{ person.student.local_addr_city }},
                {{ person.student.local_addr_state }}
                {{ person.student.local_addr_5digit_zip }},
                {{ person.student.local_addr_country }}
              </address>
            </li>
            <li>
              <b>Permanet Address: </b>
              <address>
                {{ person.student.perm_addr_line1 }}
                {{ person.student.perm_addr_line2 }},
                {{ person.student.perm_addr_city }},
                {{ person.student.perm_addr_state }}
                {{ person.student.perm_addr_5digit_zip }},
                {{ person.student.perm_addr_country }}
              </address>
            </li>
            <li>
              <b>Parent Address: </b>
              <address>
                {{ person.student.parent_addr_line1 }}
                {{ person.student.parent_addr_line2 }},
                {{ person.student.parent_addr_city }},
                {{ person.student.parent_addr_state }}
                {{ person.student.parent_addr_5digit_zip }},
                {{ person.student.parent_addr_country }}
              </address>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  {{ mq }}
</template>

<script>
export default {
  inject: ["mq"],
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

<style lang="scss" scoped>
.img-profile {
  height: 120px;
  width: 120px;
  object-fit: cover;
  object-position: top;
}
</style>
