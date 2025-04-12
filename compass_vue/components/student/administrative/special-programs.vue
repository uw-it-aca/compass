<template>
  <BCard
    class="shadow-sm rounded-3"
    header-class="p-3"
    header-bg-variant="transparent"
    footer-bg-variant="transparent"
  >
    <template #header>
      <div class="fs-6 fw-bold">Special Programs</div>
    </template>

    <ul class="list-unstyled">
      <li>
        Code: {{ person.student.special_program_code }} -
        {{ person.student.special_program_desc }}
      </li>
    </ul>
    <!-- MARK: if now affiliation date set -->
    <div v-if="programData.program_date">
      <p>
        This student affiliated on<br />
        <span class="fw-bold">{{
          formatDate(programData.program_date, "MMMM D, YYYY")
        }}</span>
      </p>
      <div class="my-3 text-end">
        <SpecialProgramEdit
          :person="person"
          :program-data="programData"
          @special-program-updated="loadSpecialProgramData()"
        >
          <i class="bi bi-pencil me-2"></i>Edit
        </SpecialProgramEdit>
        <SpecialProgramDelete
          :person="person"
          :program-data="programData"
          @special-program-updated="loadSpecialProgramData()"
        >
          <i class="bi bi-trash ms-e"></i>Delete
        </SpecialProgramDelete>
      </div>
      <p v-if="programData.modified_by" class="small text-muted m-0">
        Last updated by:
        <span class="text-muted">{{ programData.modified_by.uwnetid }}</span>
      </p>
    </div>
    <!-- MARK: set affiliation date -->
    <div v-else>
      <div class="mt-3">
        <p class="text-muted">
          No affiliation date has been set for this student.
        </p>
        <div class="text-end">
          <SpecialProgramAdd
            :person="person"
            :program-data="programData"
            @special-program-updated="loadSpecialProgramData()"
          >
            <i class="bi bi-calendar-plus-fill me-2"></i>Add affiliation date
          </SpecialProgramAdd>
        </div>
      </div>
    </div>
  </BCard>
</template>

<script>
import { formatDate } from "@/utils/dates";
import { getStudentSpecialProgram } from "@/utils/data";
import SpecialProgramAdd from "@/components/student/administrative/special-programs-add.vue";
import SpecialProgramEdit from "@/components/student/administrative/special-programs-edit.vue";
import SpecialProgramDelete from "@/components/student/administrative/special-programs-delete.vue";

import { BCard } from "bootstrap-vue-next";

export default {
  components: {
    BCard,
    SpecialProgramAdd,
    SpecialProgramEdit,
    SpecialProgramDelete,
  },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return {
      formatDate,
      getStudentSpecialProgram,
    };
  },
  data() {
    return {
      userNetid: document.body.getAttribute("data-user-netid"),
      userRole: document.body.getAttribute("data-user-role"),
      programData: { program_date: null },
    };
  },
  created() {
    this.loadSpecialProgramData();
  },
  methods: {
    loadSpecialProgramData() {
      this.getStudentSpecialProgram(this.person.student.system_key)
        .then((response) => {
          this.programData = response;
        })
        .catch((error) => {
          if (error.response.status === 404) {
            this.programData = { program_date: null };
          } else {
            console.log(
              "Cannot get special program metadata for " +
                this.person.student.system_key +
                ": " +
                error.response
            );
          }
        });
    },
  },
};
</script>
