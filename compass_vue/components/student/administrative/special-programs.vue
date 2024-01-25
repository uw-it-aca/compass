<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Special Programs</axdd-card-heading>
    </template>
    <template #body>
      <ul class="list-unstyled">
        <li>
          Code: {{ person.student.special_program_code }} -
          {{ person.student.special_program_desc }}
        </li>
      </ul>
      <!-- MARK: if now affiliation date set -->
      <div class="mb-3" v-if="program_data.program_date">
        <div class="small">
          <strong>Affiliation Date:</strong>
          <span class="ms-2">{{ formatDate(program_data.program_date, "MMMM D, YYYY") }}</span><br />
          <span v-if="program_data.modified_by">Modified by: <span class="text-muted">{{ program_data.modified_by.uwnetid }}</span></span>
        </div>
        <div class="mt-2 text-end">
          <SpecialProgramEdit
            :button-type="'button'"
            :person="person"
            :program_data="program_data"
            @specialProgramUpdated="loadSpecialProgramData()"
          >
            <i class="bi bi-pencil me-2"></i>Edit
          </SpecialProgramEdit>
          <SpecialProgramDelete
            :button-type="'button'"
            :person="person"
            :program_data="program_data"
            @specialProgramUpdated="loadSpecialProgramData()"
          >
            <i class="bi bi-trash ms-e"></i>Delete
          </SpecialProgramDelete>
        </div>
      </div>
      <!-- MARK: set affiliation date -->
      <div v-else>
        <div class="mt-3 text-center">
          <SpecialProgramEdit
            :button-type="'button'"
            :person="person"
            :program_data="program_data"
            @specialProgramUpdated="loadSpecialProgramData()"
          >
            <i class="bi bi-pencil me-2"></i>Add Affiliation Date
          </SpecialProgramEdit>
        </div>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import { formatDate } from "@/utils/dates";
import { getStudentSpecialProgram } from "@/utils/data";
import SpecialProgramEdit from "@/components/student/administrative/special-programs-edit.vue";
import SpecialProgramDelete from "@/components/student/administrative/special-programs-delete.vue";


export default {
  components: {
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
      getStudentSpecialProgram
    };
  },
  data() {
    return {
      userNetid: document.body.getAttribute("data-user-netid"),
      userRole: document.body.getAttribute("data-user-role"),
      program_data: { program_date: null },
    };
  },
  created() {
    this.loadSpecialProgramData();
  },
  methods: {
    loadSpecialProgramData() {
      this.getStudentSpecialProgram(this.person.student.system_key,
          this.person.student.special_program_code).then(
        (response) => {
          this.program_data = response.data;
        }
      )
      .catch((error) => {
        if (error.response.status === 404) {
              this.program_data = { program_date: null };
        } else {
          console.log('Cannot get special program metadata for '
          + this.person.student.system_key + ': ' + error.response.data);
        }
      });
    },
  },
};
</script>
