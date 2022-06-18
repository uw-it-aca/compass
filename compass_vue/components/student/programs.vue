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
      <div class="border p-1 small mt-3">
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
              value
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
        <div class="mt-3">
          <button type="button" class="btn btn-outline-dark-beige btn-sm">
            Update programs
          </button>
        </div>
      </div>

      <div class="border p-1 small mt-3">
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
              value
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
        <div class="mt-3">
          <button type="button" class="btn btn-outline-dark-beige btn-sm">
            Update programs
          </button>
        </div>
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
    studentPrograms: {
      type: Object,
      required: true,
    },
    studentSpecialPrograms: {
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
  },
};
</script>
