<template>
  <div class="bg-light-gray rounded-3">
    <div class="p-3 row">
      <div class="col-xl-3 my-auto">
        <div class="text-center">
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
          <div class="h4 text-secondary axdd-font-encode-sans mb-2">
            <template v-if="person.pronouns">
              {{ person.pronouns }}
            </template>
            <template v-else>He/Him</template>
          </div>
          <div class="mt-3">
            {{ person.student.student_number }},
            {{ person.student.student_email }}
          </div>
        </div>
      </div>
      <div class="col-xl-3">
        <div class="p-3 mt-2">
          <div class="flex-fill">
            <div class="fw-bold text-dark-beige mb-1" v-if="mq.xl">
              Personal Information
            </div>
            <ul class="list-unstyled m-0">
              <!-- {{ person.full_name }} -->
              <li><b>Full name: </b>Jamesy Jimmy McJames</li>
              <li><b>First: </b>{{ person.first_name }}</li>
              <li><b>Last: </b>{{ person.surname }}</li>
              <li><b>Gender: </b>{{ person.student.gender }}</li>
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
      <!-- show line during mobile view-->
      <div class="m-0" v-if="!mq.xl" aria-hidden="true"><hr /></div>
      <div class="col-12 col-xl-3">
        <div class="p-3 mt-2 v-if="!mq.xl"">
          <div class="fw-bold text-dark-beige mb-1" v-if="mq.xl">
            Immigration Status
          </div>
          <ul class="list-unstyled m-0">
            <li>
              <strong>Citizenship: </strong>
              {{ person.student.citizen_country }}
            </li>
            <li>
              <strong>Visa Type: </strong>
              <span v-if="person.student.visa_type">
                {{ person.student.visa_type }}
              </span>
              <span v-else> N/A </span>
            </li>
            <li>
              <strong>Residency: </strong>{{ person.student.resident_desc }}
            </li>
          </ul>
        </div>
        <div v-if="!mq.xl" aria-hidden="true"><hr /></div>
        <div class="p-3 mt-2">
          <div class="fw-bold text-dark-beige mb-1" v-if="mq.xl">
            Emergency Contact
          </div>
          <ul class="list-unstyled m-0">
            <li><strong>Name: </strong> {{ person.student.emergency_name }}</li>
            <li>
              <strong>Phone: </strong>
              <span v-if="person.student.visa_type">
                {{ person.student.emergency_phone }}
              </span>
              <span v-else> N/A </span>
            </li>
            <li>
              <span v-if="person.student.emergency_email">
                <strong>Email: </strong>{{ person.student.emergency_email }}
              </span>
              <span v-else
                ><strong>Email: </strong>hossain.anowar78@yahoo.com</span
              >
            </li>
          </ul>
        </div>
      </div>
      <div v-if="!mq.xl" aria-hidden="true"><hr /></div>
      <div class="col-12 col-xl-3">
        <div class="p-3 mt-2">
          <p class="text-dark-beige fw-bold mb-1" v-if="mq.xl">Address</p>
          <ul class="list-unstyled m-0">
            <li>
              <b>Local Address: </b>
              <address>
                {{ person.student.local_addr_line1 }}
                {{ person.student.local_addr_line2 }},
                {{ person.student.local_addr_city }},
                {{ person.student.local_addr_state }}
                {{ person.student.local_addr_5digit_zip }}
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
                {{ person.student.perm_addr_5digit_zip }}
                {{ person.student.perm_addr_country }}
              </address>
            </li>
            <li>
              <strong>Parent Address: </strong><br />
              <span v-if="person.student.parent_addr_line1">
                <address>
                  {{ person.student.parent_addr_line1 }}
                  {{ person.student.parent_addr_line2 }},
                  {{ person.student.parent_addr_city }},
                  {{ person.student.parent_addr_state }}
                  {{ person.student.parent_addr_5digit_zip }},
                  {{ person.student.parent_addr_country }}
                </address>
              </span>
              <span v-else>N/A</span>
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
