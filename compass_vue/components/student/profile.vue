<template>
  <div class="bg-light rounded-3 border-0 px-0 py-4 m-0">
    <div class="row">
      <div class="col-xl-3 my-auto">
        <div class="text-center mb-4">
          <div class="d-inline-block rounded-circle border border-4 mb-2">
            <img
              :src="person.photo_url"
              @error="$event.target.src = '/static/compass/img/placeholder.png'"
              class="img-profile rounded-circle border bg-light border-white border-2"
            />
          </div>
          <!-- moved preferred name to under the profile photo -->
          <div class="h4 axdd-font-encode-sans mb-0">
            <template v-if="person.display_name">
              {{ person.display_name }}
            </template>
            <template v-else>{{ person.full_name }}</template>
          </div>
          <!-- moved pronouns to under the preferred name -->
          <div class="text-secondary mb-2">
            <template v-if="person.pronouns">
              {{ person.pronouns }}
            </template>
            <template v-else>not/specified</template>
          </div>
          <div class="mt-3 small">
            {{ person.student.student_number }}, {{ person.uwnetid }}<br />
            <span v-if="person.student.local_phone_number">
              +1 {{ person.student.local_phone_number }}
            </span>
          </div>
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
          <hr class="text-muted" />
        </div>
      </div>

      <div class="col-xl-3">
        <div class="flex-fill px-3">
          <div
            v-if="mq.xlPlus"
            class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
          >
            Legal Name
          </div>
          <ul class="list-unstyled m-0 small mb-3">
            <li>
              <KeyValue>
                <template #key>Full Name </template>
                <template #value> {{ person.full_name }} </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key>First Name </template>
                <template #value> {{ person.first_name }} </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key>Last Name </template>
                <template #value> {{ person.surname }} </template>
              </KeyValue>
            </li>
          </ul>

          <div
            v-if="mq.xlPlus"
            class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
          >
            Personal Information
          </div>
          <ul class="list-unstyled m-0 small">
            <li>
              <KeyValue>
                <template #key>Gender</template>
                <template #value> {{ person.student.gender }} </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key>DOB</template>
                <template #value> {{ person.student.birthdate }} </template>
              </KeyValue>
            </li>
            <li
              v-for="(ethinicity, index) in person.student.ethnicities"
              :key="index"
            >
              <KeyValue>
                <template #key>Ethnicity</template>
                <template #value>
                  {{ ethinicity.assigned_ethnic_group_desc }}
                </template>
              </KeyValue>
            </li>
            <li class="mt-3">
              <KeyValue>
                <template #key>Disability</template>
                <template #value>
                  {{ person.student.disability_ind }}
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key>Veteran Status</template>
                <template #value>
                  <span>
                    {{ person.student.veteran_desc }}
                  </span>
                </template>
              </KeyValue>
            </li>
            <li class="mb-3">
              <KeyValue>
                <template #key>Veteran Benefit</template>
                <template #value>
                  <span>{{ person.student.veteran_benefit_desc }}</span>
                </template>
              </KeyValue>
            </li>
          </ul>
        </div>

        <div class="px-3">
          <div
            v-if="mq.xlPlus"
            class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
          >
            Athletics
          </div>
          <ul class="list-unstyled m-0 small">
            <li class="mb-3">
              <KeyValue>
                <template #key>Sports</template>
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
          </ul>
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
          <hr class="text-muted" />
        </div>
      </div>

      <div class="col-12 col-xl-3">
        <div class="px-3">
          <div
            v-if="mq.xlPlus"
            class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
          >
            Immigration
          </div>
          <ul class="list-unstyled m-0 mb-3 small">
            <li>
              <KeyValue>
                <template #key>Citizenship</template>
                <template #value>
                  {{ person.student.citizen_country }}
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key>Visa Type</template>
                <template #value>
                  <span v-if="person.student.visa_type">
                    {{ person.student.visa_type }}
                  </span>
                  <span v-else>N/A</span>
                </template>
              </KeyValue>
            </li>
          </ul>
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
          <hr class="text-muted" />
        </div>

        <div class="px-3">
          <div
            v-if="mq.xlPlus"
            class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
          >
            Residency
          </div>
          <ul class="list-unstyled m-0 small">
            <li class="mb-3">
              <KeyValue>
                <template #key>Status</template>
                <template #value>
                  {{ person.student.resident_desc }}
                </template>
              </KeyValue>
            </li>
          </ul>
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
          <hr class="text-muted" />
        </div>

        <div class="px-3">
          <div
            v-if="mq.xlPlus"
            class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
          >
            Emergency Contact
          </div>
          <ul class="list-unstyled m-0 small">
            <li>
              <KeyValue>
                <template #key>Name</template>
                <template #value>
                  {{ person.student.emergency_name }}
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key>Phone</template>
                <template #value>
                  {{ person.student.emergency_phone }}
                </template>
              </KeyValue>
            </li>
            <li>
              <span v-if="person.student.emergency_email.length > 25">
                <KeyValue variant="address">
                  <template #key>Email</template>
                  <template #value>
                    {{ person.student.emergency_email }}
                  </template>
                </KeyValue>
              </span>
              <span v-else>
                <KeyValue>
                  <template #key>Email</template>
                  <template #value>
                    {{ person.student.emergency_email }}
                  </template>
                </KeyValue>
              </span>
            </li>
          </ul>
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
          <hr class="text-muted" />
        </div>
      </div>

      <div class="col-12 col-xl-3">
        <div class="px-3">
          <div
            v-if="mq.xlPlus"
            class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
          >
            Address
          </div>
          <ul class="list-unstyled m-0 small">
            <li>
              <KeyValue variant="address">
                <template #key>Local Address</template>
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
                <template #key>Permanent Address</template>
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
                <template #key>Parent Address</template>
                <template #value>
                  <address>
                    {{ person.student.parent_addr_line1 }}
                    {{ person.student.parent_addr_line2 }},
                    {{ person.student.parent_addr_city }},
                    {{ person.student.parent_addr_state }}
                    {{ person.student.parent_addr_5digit_zip }},
                    {{ person.student.parent_addr_country }}
                  </address>
                </template>
              </KeyValue>
            </li>
          </ul>
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
          <hr class="text-muted" />
        </div>
      </div>
    </div>
  </div>
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
