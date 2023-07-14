<template>
  <div class="bg-light rounded-3 border-0 px-0 py-4 m-0">
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
            <div class="d-inline-block rounded-circle border border-4 mb-2">
              <img
                :src="person.photo_url"
                @error="
                  $event.target.src = '/static/compass/img/placeholder.png'
                "
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
            <div class="text-secondary text-capitalize mb-2">
              <template v-if="person.pronouns">
                {{ person.pronouns }}
              </template>
            </div>
            <div class="mt-3 small">
              {{ person.student.student_number }}, {{ person.uwnetid }}<br />
              <span v-if="person.student.local_phone_number">
                +1 {{ person.student.local_phone_number }}
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
          <ProfileNameCard :person="person" />

          <ProfileInfoCard :person="person" />

          <ProfileAthleticsCard
            v-if="person.student.sports.length > 0"
            :person="person"
          />
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
          <hr class="text-muted" />
        </div>
      </div>

      <div class="col-12 col-xl-3">
        <div class="px-3">
          <ProfileImmigrationCard :person="person" />

          <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
            <hr class="text-muted" />
          </div>

          <ProfileResidencyCard :person="person" />

          <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
            <hr class="text-muted" />
          </div>

          <ProfileContactCard :person="person" />
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
          <hr class="text-muted" />
        </div>
      </div>

      <div class="col-12 col-xl-3">
        <div class="px-3">
          <ProfileAddressCard :person="person" />
        </div>

        <div v-if="!mq.xlPlus" aria-hidden="true" class="mx-3">
          <hr class="text-muted" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ProfileNameCard from "./cards/profile-name-card.vue";
import ProfileInfoCard from "./cards/profile-info-card.vue";
import ProfileAthleticsCard from "./cards/profile-athletics-card.vue";
import ProfileImmigrationCard from "./cards/profile-immigration-card.vue";
import ProfileResidencyCard from "./cards/profile-residency-card.vue";
import ProfileContactCard from "./cards/profile-contact-card.vue";
import ProfileAddressCard from "./cards/profile-address-card.vue";
import { translateTrueFalse } from "../../../utils/translations";
import { formatDate } from "../../../utils/dates";

export default {
  inject: ["mq"],
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {
    ProfileNameCard,
    ProfileInfoCard,
    ProfileAthleticsCard,
    ProfileImmigrationCard,
    ProfileResidencyCard,
    ProfileContactCard,
    ProfileAddressCard,
  },
  setup() {
    return {
      translateTrueFalse,
      formatDate,
    };
  },
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
