<template>
  <BCard
    class="shadow-sm rounded-3"
    header-class="p-3"
    header-bg-variant="transparent"
  >
    <template #header><div class="fs-6 fw-bold">Adviser</div></template>

    <div v-if="advisers">
      <ul class="list-unstyled mb-0">
        <!-- loop advisers and display OMAD adviser first -->
        <template v-for="adviser in advisers" :key="adviser.id">
          <li v-if="adviser.advising_program == 'OMAD Advising'" class="mb-3">
            <div class="d-flex">
              <i class="bi bi-person-square text-body-tertiary me-3"></i>
              <div class="flex-fill">
                <strong>{{ formatAdviserName(adviser.employee.person) }}</strong>
                ({{ adviser.employee.person.uwnetid }})<br /><span
                  class="small text-muted text-capitalize"
                  >{{ adviser.employee.person.pronouns }}</span
                >
              </div>
            </div>
            <div>
              <i class="bi bi-envelope-fill text-body-tertiary me-3"></i>
              <span>{{ adviser.advising_email }}</span>
            </div>
            <div>
              <i class="bi bi-telephone text-body-tertiary me-3"></i>
              <span>{{ adviser.advising_phone_number }}</span>
            </div>
            <div>
              <i class="bi bi-building text-body-tertiary me-3"></i>
              <span>{{ adviser.advising_program }}</span>
            </div>
          </li>
        </template>
        <template v-for="adviser in advisers" :key="adviser.id">
          <li v-if="adviser.advising_program != 'OMAD Advising'" class="mb-3">
            <div class="d-flex">
              <i class="bi bi-person-square text-body-tertiary me-3"></i>
              <div class="flex-fill">
                <strong>{{ formatAdviserName(adviser.employee.person) }}</strong>
                ({{ adviser.employee.person.uwnetid }})<br /><span
                  class="small text-muted text-capitalize"
                  >{{ adviser.employee.person.pronouns }}</span
                >
              </div>
            </div>
            <div>
              <i class="bi bi-envelope-fill text-body-tertiary me-3"></i>
              <span>{{ adviser.advising_email }}</span>
            </div>
            <div>
              <i class="bi bi-telephone text-body-tertiary me-3"></i>
              <span>{{ adviser.advising_phone_number }}</span>
            </div>
            <div>
              <i class="bi bi-building text-body-tertiary me-3"></i>
              <span>{{ adviser.advising_program }}</span>
            </div>
          </li>
        </template>
      </ul>
    </div>
    <div v-else>No adviser assigned to this student.</div>
  </BCard>
</template>

<script>
import { formatAdviserName } from "@/utils/formats";
import { BCard } from "bootstrap-vue-next";

export default {
  name: "StudentAdviser",
  components: {
    BCard,
  },
  props: {
    advisers: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return {
      formatAdviserName,
    };
  },
  data() {
    return {
      userNetid: document.body.getAttribute("data-user-netid"),
      userRole: document.body.getAttribute("data-user-role"),
    };
  },
};
</script>
