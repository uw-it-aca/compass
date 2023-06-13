<template>
  <axdd-card v-if="groupedPrograms">
    <template #heading>
      <axdd-card-heading :level="2">Programs</axdd-card-heading>
    </template>
    <template #body>
      <div
        class="alert alert-success py-2 small"
        role="alert"
        v-show="updateSuccessful"
      >
        Update Successful!
      </div>
      <div
        class="alert alert-danger py-2 small"
        role="alert"
        v-show="updatePermissionDenied"
      >
        You don't have permission to update programs.
      </div>
      <div class="mb-3">
        <template
          v-for="(groupPrograms, accessGroupName) in groupedPrograms"
          :key="accessGroupName"
        >
          <div class="fw-bold text-muted mb-2">
            {{ accessGroupName }} Programs
          </div>

          <ul class="list-group list-group-flush mb-4">
            <li
              v-for="program in groupPrograms"
              :key="program.name"
              class="list-group-item border-0 px-0 py-1 d-flex"
            >
              <label
                class="form-check-label flex-fill"
                :for="'defaultCheck' + program.name"
              >
                {{ program.name }}
              </label>
              <div class="form-check form-switch m-0">
                <input
                  class="form-check-input flex-fill"
                  type="checkbox"
                  role="switch"
                  v-model="studentPrograms"
                  :value="program.id"
                  :id="'defaultCheck' + program.name"
                  :disabled="userName != userOverride"
                />
              </div>
            </li>
          </ul>
        </template>
      </div>
      <div class="text-end">
        <button
          v-if="userName == userOverride"
          @click="saveStudentData()"
          type="button"
          class="btn btn-sm btn-outline-gray text-dark rounded-3 px-3 py-2"
        >
          Update programs
        </button>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import dataMixin from "../../mixins/data_mixin.js";
import { useAffiliationStore } from "../../../stores/affiliations";

export default {
  mixins: [dataMixin],
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {},
  data() {
    return {
      groupedPrograms: this.person.student.compass_group_affiliations,
      studentPrograms: this.person.student.compass_affiliations,
      updateSuccessful: false,
      updatePermissionDenied: false,
      userName: document.body.getAttribute("data-user-netid"),
      userOverride: document.body.getAttribute("data-user-override"),
    };
  },
  setup() {
    const storeAffiliations = useAffiliationStore();
    return { storeAffiliations };
  },
  created: function () {
    this.loadPrograms();
  },
  methods: {
    _groupProgramsByAccessGroup: function (programs) {
      return programs.reduce((groups, item) => {
        const group = groups[item.access_group.name] || [];
        group.push(item);
        groups[item.access_group.name] = group;
        return groups;
      }, {});
    },
    loadPrograms: function () {
      console.log('lp')
      var _this = this;
      this.storeAffiliations.getAffiliations.then(() => {
        _this.groupedPrograms = Object.assign(
          {},
          _this.groupedPrograms,
          _this._groupProgramsByAccessGroup(this.storeAffiliations.affiliations.data)
        );
      });
    },
    saveStudentData: function () {
      this.saveStudent(
        this.person.student.system_key,
        this.person.uwnetid,
        this.studentPrograms
      )
        .then((response) => {
          if (response.data) {
            // show and update successful message for 3 seconds
            this.updateSuccessful = true;
            setTimeout(() => (this.updateSuccessful = false), 3000);
          }
        })
        .catch((error) => {
          if (error.response.status == 401) {
            this.updatePermissionDenied = true;
            setTimeout(() => (this.updatePermissionDenied = false), 3000);
          }
        });
    },
  },
};
</script>

<style lang="scss">
.form-switch .form-check-input:checked {
  background-color: #4d307f;
  border-color: #4d307f;
}
</style>
