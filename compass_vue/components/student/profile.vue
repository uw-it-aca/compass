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

        <div v-if="!mq.xlPlus" aria-hidden="true" class="mt-4">
          <hr class="text-muted" />
        </div>
      </div>

      <div class="col-xl-3">
        <div class="flex-fill p-3">
          <div v-if="mq.xlPlus" class="fw-bold text-dark-beige mb-1">
            Personal Information
          </div>
          <ul class="list-unstyled m-0">
            <li>
              <KeyValue>
                <template #key> Full Name</template>
                <template #value> {{ person.full_name }} </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> First Name: </template>
                <template #value> {{ person.first_name }} </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> Last Name: </template>
                <template #value> {{ person.surname }} </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> Gender: </template>
                <template #value> {{ person.gender }} </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> DOB: </template>
                <template #value> {{ person.student.birthdate }} </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> Ethnicity: </template>
                <template #value>
                  {{ person.student.assigned_ethnic_desc }}
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> Disabled: </template>
                <template #value>
                  <span v-if="person.student.disability_ind"> Disabled</span>
                  <span v-else> Not Disabled </span>
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> Veterans: </template>
                <template #value>
                  <span v-if="person.student.veteran_benefit_code === '0'">
                    Not A Vet</span
                  >
                  <span v-else>
                    {{ person.student.veteran_benefit_code }},
                    {{ person.student.veteran_benefit_desc }},
                    {{ person.student.veteran_desc }}
                  </span>
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> Athelete: </template>
                <template #value>
                  <span
                    v-for="(sport, index) in person.student.sports"
                    :key="sport.code"
                  >
                    {{ sport.sport_code }}
                    <span v-if="index + 1 < person.student.sports.length"
                      >,
                    </span>
                  </span>
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> Phone: </template>
                <template #value>
                  +1 {{ person.student.local_phone_number }}
                </template>
              </KeyValue>
            </li>
          </ul>
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true">
          <hr class="text-muted" />
        </div>
      </div>

      <div class="col-12 col-xl-3">
        <div class="p-3">
          <div v-if="mq.xlPlus" class="fw-bold text-dark-beige mb-1">
            Immigration Status
          </div>
          <ul class="list-unstyled m-0">
            <li>
              <KeyValue>
                <template #key> Citizenship: </template>
                <template #value>
                  {{ person.student.citizen_country }}
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> Visa Typw: </template>
                <template #value>
                  <span v-if="person.student.visa_type">
                    {{ person.student.visa_type }}
                  </span>
                  <span v-else> N/A </span>
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> Citizenship: </template>
                <template #value>
                  {{ person.student.resident_desc }}
                </template>
              </KeyValue>
            </li>
          </ul>
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true">
          <hr class="text-muted" />
        </div>

        <div class="p-3">
          <div v-if="mq.xlPlus" class="fw-bold text-dark-beige mb-1">
            Emergency Contact
          </div>
          <ul class="list-unstyled m-0">
            <li>
              <KeyValue>
                <template #key> Name: </template>
                <template #value>
                  {{ person.student.emergency_name }}
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> Phone: </template>
                <template #value>
                  {{ person.student.emergency_phone }}
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key> Email: </template>
                <template #value>
                  {{ person.student.emergency_email }}
                </template>
              </KeyValue>
            </li>
          </ul>
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true">
          <hr class="text-muted" s />
        </div>
      </div>

      <div class="col-12 col-xl-3">
        <div class="p-3">
          <p v-if="mq.xlPlus" class="text-dark-beige fw-bold mb-1">Address</p>
          <ul class="list-unstyled m-0">
            <li>
              <KeyValue variant="address">
                <template #key> Local Address: </template>
                <template #value>
                  <address>
                    {{ person.student.local_addr_line1 }}
                    {{ person.student.local_addr_line2 }},
                    {{ person.student.local_addr_city }},
                    {{ person.student.local_addr_state }}
                    {{ person.student.local_addr_5digit_zip }}
                    {{ person.student.local_addr_country }}
                  </address>
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue variant="address">
                <template #key> Permanent Address: </template>
                <template #value>
                  <address>
                    {{ person.student.perm_addr_line1 }}
                    {{ person.student.perm_addr_line2 }},
                    {{ person.student.perm_addr_city }},
                    {{ person.student.perm_addr_state }}
                    {{ person.student.perm_addr_5digit_zip }}
                    {{ person.student.perm_addr_country }}
                  </address>
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue variant="address">
                <template #key> Parent Address: </template>
                <template #value>
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
                </template>
              </KeyValue>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  {{ mq }}
</template>

<script>
import KeyValue from "../../components/_common/key-value.vue";

export default {
  inject: ["mq"],
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: { KeyValue },
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
