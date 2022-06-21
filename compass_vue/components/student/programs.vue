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
      <div class="border p-1 mb-3 small">
        <template
          v-for="(groupPrograms, accessGroupName) in groupedPrograms"
          :key="accessGroupName"
        >
          <div class="fw-bold">{{ accessGroupName }} Programs</div>
          <div
            class="form-check"
            v-for="program in groupPrograms"
            :key="program.name"
          >
            <input
              class="form-check-input"
              type="checkbox"
              v-model="studentPrograms"
              :value="program.id"
              :id="'defaultCheck' + program.name"
            />
            <label
              class="form-check-label"
              :for="'defaultCheck' + program.name"
            >
              {{ program.name }}
            </label>
          </div>
        </template>
      </div>
      <div>
        <button
          @click="saveStudentData()"
          type="button"
          class="btn btn-outline-dark-beige btn-sm"
        >
          Update programs
        </button>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import dataMixin from "../../mixins/data_mixin.js";
import { Card, CardHeading } from "axdd-components";

export default {
  mixins: [dataMixin],
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
  },
  data() {
    return {
      programs: {},
      studentPrograms: this.person.student.compass_programs,
      updateSuccessful: false,
    };
  },
  created: function () {
    this.loadPrograms();
  },
  computed: {
    groupedPrograms() {
      if (this.programs.length) {
        return this._groupAccessGroup(this.programs);
      } else {
        return {};
      }
    },
  },
  methods: {
    _groupAccessGroup: function (accessGroup) {
      return accessGroup.reduce((groups, item) => {
        const group = groups[item.access_group.name] || [];
        group.push(item);
        groups[item.access_group.name] = group;
        return groups;
      }, {});
    },
    loadPrograms: function () {
      this.getPrograms().then((response) => {
        if (response.data) {
          this.programs = response.data;
        }
      });
    },
    saveStudentData: function () {
      this.saveStudent(
        this.person.student.system_key,
        this.studentPrograms
      ).then((response) => {
        if (response.data) {
          // show and update successful message for 3 seconds
          this.updateSuccessful = true;
          setTimeout(() => (this.updateSuccessful = false), 3000);
        }
      });
    },
  },
};
</script>
