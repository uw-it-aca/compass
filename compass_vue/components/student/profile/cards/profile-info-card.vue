<template>
  <div
    v-if="mq.xlPlus"
    class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
  >
    Personal Information
  </div>
  <ul class="list-unstyled m-0 small">
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
          {{ person.student.ethnic_long_desc }},
          {{ person.student.ethnic_group_code }},
          {{ person.student.ethnic_group_desc }}
        </template>
      </KeyValue>
    </li>
    <li>
      <KeyValue>
        <template #key>Hispanic</template>
        <template #value>
          {{ person.student.hispanic_code }},
          {{ person.student.hispanic_desc }},
          {{ person.student.hispanic_long_desc }},
          {{ person.student.hispanic_group_code }},
          {{ person.student.hispanic_group_desc }}
        </template>
      </KeyValue>
    </li>
    <li class="mt-3">
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
    <li class="mb-3">
      <KeyValue>
        <template #key>Veteran Benefit</template>
        <template #value>
          <span>{{ person.student.veteran_benefit_desc }}</span>
        </template>
      </KeyValue>
    </li>
  </ul>
</template>

<script>
import KeyValue from "@/components/_common/key-value.vue";

export default {
  inject: ["mq"],
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {
    KeyValue,
  },
  data() {
    return {};
  },
  methods: {
    translateTrueFalse(value) {
      if (value === "Y") {
        return "Yes";
      } else if (value === "N") {
        return "No";
      } else {
        return "Unknown";
      }
    },
  },
};
</script>
