<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Programs</axdd-card-heading>
    </template>
    <template #body>
      <ul class="list-unstyled small">
        <li>
          EDW Special Program Code:
          <template v-if="person.student.transcripts">
            {{ person.student.transcripts[0].special_program }}
          </template>
        </li>
      </ul>
      <div v-if="groupedSpecialPrograms" class="border p-1 small mt-3">
        <template
          v-for="(groupPrograms, accessGroupName) in groupedSpecialPrograms"
          :key="accessGroupName"
        >
          <div class="fw-bold">{{ accessGroupName }} Special Programs</div>
          <div
            class="form-check"
            v-for="program in groupPrograms"
            :key="program.name"
          >
            <input
              class="form-check-input"
              type="checkbox"
              v-model="studentSpecialPrograms"
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

      <div v-if="groupedPrograms" class="border p-1 small mt-3">
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
      <div class="mt-3">
        <button
          @click="saveStudentData()"
          type="button"
          class="btn btn-outline-dark-beige btn-sm"
        >
          Update programs
        </button>
        <span class="mt-3 badge alert-success" v-show="updateSuccessful">
          Update Successful
        </span>
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
      specialPrograms: {},
      studentPrograms: this.person.student.compass_programs,
      studentSpecialPrograms: this.person.student.compass_special_programs,
      updateSuccessful: false,
    };
  },
  created: function () {
    this.loadPrograms();
    this.loadSpecialPrograms();
  },
  computed: {
    groupedPrograms() {
      if (this.programs.length) {
        return this._groupAccessGroup(this.programs);
      } else {
        return {};
      }
    },
    groupedSpecialPrograms() {
      if (this.specialPrograms.length) {
        return this._groupAccessGroup(this.specialPrograms);
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
      let _this = this;
      this.getPrograms().then((response) => {
        if (response.data) {
          _this.programs = response.data;
        }
      });
    },
    loadSpecialPrograms: function () {
      let _this = this;
      this.getSpecialPrograms().then((response) => {
        if (response.data) {
          _this.specialPrograms = response.data;
        }
      });
    },
    saveStudentData: function () {
      let _this = this;
      this.saveStudent(
        this.person.student.system_key,
        this.studentPrograms,
        this.studentSpecialPrograms
      ).then((response) => {
        if (response.data) {
          // show and update successful message for 3 seconds
          _this.updateSuccessful = true;
          setTimeout(() => (_this.updateSuccessful = false), 3000);
        }
      });
    },
  },
};
</script>
