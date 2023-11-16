<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Adviser</axdd-card-heading>
    </template>
    <template #body>
      <div v-if="advisers">
        <ul class="list-unstyled mb-0">
          <!-- loop advisers and display OMAD adviser first -->
          <template v-for="(adviser, index) in advisers" :key="adviser.id">
            <li
              v-if="
                adviser.employee.adviser.advising_program == 'OMAD Advising'
              "
              class="mb-3"
            >
              <div class="d-flex">
                <i class="bi bi-person-square text-gray me-3"></i>
                <div class="flex-fill">
                  <strong>{{ adviser.display_name }}</strong> ({{
                    adviser.uwnetid
                  }})<br /><span class="small text-muted text-capitalize">{{
                    adviser.pronouns
                  }}</span>
                </div>
              </div>
              <div>
                <i class="bi bi-envelope-fill text-gray me-3"></i>
                <span>{{ adviser.employee.adviser.advising_email }}</span>
              </div>
              <div>
                <i class="bi bi-telephone text-gray me-3"></i>
                <span>{{
                  adviser.employee.adviser.advising_phone_number
                }}</span>
              </div>
              <div>
                <i class="bi bi-building text-gray me-3"></i>
                <span>{{ adviser.employee.adviser.advising_program }}</span>
              </div>
            </li>
          </template>
          <template v-for="(adviser, index) in advisers" :key="adviser.id">
            <li
              v-if="
                adviser.employee.adviser.advising_program != 'OMAD Advising'
              "
              class="mb-3"
            >
              <div class="d-flex">
                <i class="bi bi-person-square text-gray me-3"></i>
                <div class="flex-fill">
                  <strong>{{ adviser.display_name }}</strong> ({{
                    adviser.uwnetid
                  }})<br /><span class="small text-muted text-capitalize">{{
                    adviser.pronouns
                  }}</span>
                </div>
              </div>
              <div>
                <i class="bi bi-envelope-fill text-gray me-3"></i>
                <span>{{ adviser.employee.adviser.advising_email }}</span>
              </div>
              <div>
                <i class="bi bi-telephone text-gray me-3"></i>
                <span>{{
                  adviser.employee.adviser.advising_phone_number
                }}</span>
              </div>
              <div>
                <i class="bi bi-building text-gray me-3"></i>
                <span>{{ adviser.employee.adviser.advising_program }}</span>
              </div>
            </li>
          </template>
        </ul>
      </div>
      <div v-else>No adviser assigned to this student.</div>
    </template>
  </axdd-card>
</template>

<script>
export default {
  props: {
    advisers: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      userNetid: document.body.getAttribute("data-user-netid"),
      userRole: document.body.getAttribute("data-user-role"),
    };
  },
  components: {},
};
</script>
