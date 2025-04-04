<template>
  <BCard class="bg-body-tertiary rounded-3" border-variant="0">
    <div class="row">
      <div class="col-xl-3 d-flex flex-column">
        <div v-if="person.student.deceased_date" class="px-3 mt-n1">
          <span
            class="badge rounded-pill text-bg-danger fw-light text-uppercase"
            >Deceased</span
          >
          <span class="ms-2 small text-muted"
            >{{ formatDate(person.student.deceased_date, "LL") }}
          </span>
        </div>
        <div class="flex-fill d-flex px-3 text-center">
          <div class="align-self-center flex-fill">
            <div
              class="d-inline-block rounded-circle border border-light-subtle border-4 mb-2"
            >
              <img
                :src="person.photo_url"
                class="img-profile rounded-circle border border-4"
                :class="borderClass"
                @error="
                  $event.target.src = '/static/compass/img/placeholder.png'
                "
              />
            </div>
            <!-- moved preferred name to under the profile photo -->
            <div class="h4 ff-encode-sans mb-0">
              <template v-if="person.display_name">
                {{ person.display_name }}
              </template>
              <template v-else>{{ person.full_name }}</template>
            </div>
            <!-- moved pronouns to under the preferred name -->
            <div class="text-light-emphasis text-capitalize mb-2">
              <template v-if="person.pronouns">
                {{ person.pronouns }}
              </template>
            </div>
            <div class="mt-3 small">
              {{ person.student.student_number }}, {{ person.uwnetid }}<br />
              <span v-if="person.student.local_phone_number">
                {{ formatPhoneNumber(person.student.local_phone_number) }}
              </span>
            </div>
          </div>
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
          <hr class="text-muted" />
        </div>
      </div>

      <div class="col-xl-3">
        <div class="flex-fill px-3">
          <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-2">
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

          <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-2">
            Personal Information
          </div>
          <ul class="list-unstyled m-0 mb-3 small">
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
            <li>
              <KeyValue>
                <template #key>Ethnicity</template>
                <template #value>
                  {{ person.student.ethnic_code }},
                  {{ person.student.ethnic_desc }},
                  {{ person.student.ethnic_long_desc }}<br />
                  {{ person.student.ethnic_group_code }},
                  {{ person.student.ethnic_group_desc }}
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue v-if="person.student.hispanic_code !== null">
                <template #key>Hispanic</template>
                <template #value>
                  {{ person.student.hispanic_code }},
                  {{ person.student.hispanic_desc }},
                  {{ person.student.hispanic_long_desc }}<br />
                  {{ person.student.hispanic_group_code }},
                  {{ person.student.hispanic_group_desc }}
                </template>
              </KeyValue>
              <KeyValue v-else>
                <template #key>Hispanic</template>
                <template #value> Not Indicated </template>
              </KeyValue>
            </li>
          </ul>

          <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-2">
            Email
          </div>
          <ul class="list-unstyled mb-3 small">
            <li>
              <KeyValue>
                <template #key>Student</template>
                <template #value
                  ><a :href="'mailto:' + person.student.student_email">{{
                    person.student.student_email
                  }}</a></template
                >
              </KeyValue>
            </li>
            <li>
              <KeyValue>
                <template #key>External</template>
                <template #value>
                  <a :href="'mailto:' + person.student.external_email">{{
                    person.student.external_email
                  }}</a>
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
          <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-2">
            Benefits
          </div>
          <ul class="list-unstyled m-0 small">
            <li>
              <KeyValue>
                <template #key>Disability</template>
                <template #value>
                  {{ translateTrueFalse(person.student.disability_ind) }}
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
            <li>
              <KeyValue v-if="person.student.veteran_benefit_code !== 0">
                <template #key>Veteran Benefits</template>
                <template #value>
                  <span
                    >{{ person.student.veteran_benefit_code }},
                    {{ person.student.veteran_benefit_desc }}</span
                  >
                </template>
              </KeyValue>
              <KeyValue v-else>
                <template #key>Veteran Benefits</template>
                <template #value>
                  <span>No</span>
                </template>
              </KeyValue>
            </li>
            <li class="mb-3">
              <KeyValue>
                <template #key>First Generation (4yr)</template>
                <template #value>
                  {{
                    translateTrueFalse(person.student.first_generation_4yr_ind)
                  }}
                </template>
              </KeyValue>
            </li>
          </ul>

          <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-2">
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

          <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-2">
            Residency
          </div>
          <ul class="list-unstyled m-0 small">
            <li class="mb-3">
              <KeyValue>
                <template #key>Status</template>
                <template #value>
                  {{ person.student.resident_code }},
                  {{ person.student.resident_desc }}
                </template>
              </KeyValue>
            </li>
          </ul>

          <template v-if="person.student.sports.length > 0">
            <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-2">
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
                      {{ sport.sport_code }}, {{ sport.sport_descrip }}
                      <span v-if="index + 1 < person.student.sports.length"
                        >,
                      </span>
                    </span>
                  </template>
                </KeyValue>
              </li>
            </ul>
          </template>
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
          <hr class="text-muted" />
        </div>
      </div>

      <div class="col-12 col-xl-3">
        <div class="px-3">
          <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-2">
            Address
          </div>
          <ul class="list-unstyled mb-3 small">
            <li class="mb-3">
              <KeyValue variant="address">
                <template #key>Local Address</template>
                <template #value>
                  <address class="mb-0">
                    <div>{{ person.student.local_addr_line1 }}</div>
                    <div v-show="person.student.local_addr_line2 !== null">
                      {{ person.student.local_addr_line2 }}
                    </div>
                    <div>
                      {{ person.student.local_addr_city
                      }}<span v-show="person.student.local_addr_state !== null"
                        >,</span
                      >
                      {{ person.student.local_addr_state }}
                      {{ person.student.local_addr_5digit_zip }}
                    </div>
                  </address>
                  <div v-show="person.student.local_phone_number !== null">
                    {{ formatPhoneNumber(person.student.local_phone_number) }}
                  </div>
                </template>
              </KeyValue>
            </li>
            <li class="mb-3">
              <KeyValue variant="address">
                <template #key>Permanent Address</template>
                <template #value>
                  <address class="mb-0">
                    <div>{{ person.student.perm_addr_line1 }}</div>
                    <div v-show="person.student.perm_addr_line2 !== null">
                      {{ person.student.perm_addr_line2 }}
                    </div>
                    <div>
                      {{ person.student.perm_addr_city
                      }}<span v-show="person.student.perm_addr_state !== null"
                        >,</span
                      >
                      {{ person.student.perm_addr_state }}
                      {{ person.student.perm_addr_5digit_zip }}
                    </div>
                    <div v-show="person.student.perm_addr_country !== null">
                      {{ person.student.perm_addr_country }}
                    </div>
                  </address>
                  <div v-show="person.student.perm_phone_number !== null">
                    {{ formatPhoneNumber(person.student.perm_phone_number) }}
                  </div>
                </template>
              </KeyValue>
            </li>
            <li>
              <KeyValue variant="address">
                <template #key>Parent Address</template>
                <template #value>
                  <div>{{ person.student.parent_name }}</div>
                  <address class="mb-0">
                    <div>{{ person.student.parent_addr_line1 }}</div>
                    <div v-show="person.student.parent_addr_line2 !== null">
                      {{ person.student.parent_addr_line2 }}
                    </div>
                    <div>
                      {{ person.student.parent_addr_city
                      }}<span v-show="person.student.parent_addr_state !== null"
                        >,</span
                      >
                      {{ person.student.parent_addr_state }}
                      {{ person.student.parent_addr_5digit_zip }}
                    </div>
                    <div v-show="person.student.parent_addr_country !== null">
                      {{ person.student.parent_addr_country }}
                    </div>
                  </address>
                  <div v-show="person.student.parent_phone_number !== null">
                    {{ formatPhoneNumber(person.student.parent_phone_number) }}
                  </div>
                </template>
              </KeyValue>
            </li>
          </ul>

          <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-2">
            Emergency Contact
          </div>

          <ul class="list-unstyled m-0 small mb-3">
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
                  {{ formatPhoneNumber(person.student.emergency_phone) }}
                </template>
              </KeyValue>
            </li>
            <li>
              <span v-if="person.student.emergency_email.length > 25">
                <KeyValue>
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
      </div>
    </div>
  </BCard>
</template>

<script>
import KeyValue from "@/components/_common/key-value.vue";
import { translateTrueFalse } from "@/utils/translations";
import { formatDate } from "@/utils/dates";
import { formatPhoneNumber } from "@/utils/formats";
import { BCard } from "bootstrap-vue-next";

export default {
  name: "StudentProfile",
  components: { KeyValue, BCard },
  inject: ["mq"],
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return {
      translateTrueFalse,
      formatDate,
      formatPhoneNumber,
    };
  },
  data() {
    return {};
  },
  computed: {
    borderClass() {
      const classes = {
        danger: "border-danger",
        warning: "border-warning",
        normal: "border-success",
      };
      return classes[this.person.analytics_alert] || classes.normal;
    },
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
