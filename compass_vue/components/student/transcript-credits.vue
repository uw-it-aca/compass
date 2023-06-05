<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Credit summary</axdd-card-heading>
    </template>
    <template #body>
      <ul class="list-unstyled">
        <li>
          <div class="d-flex justify-content-between">
            <span>UW Credits Attempted:</span>
            <span>xxx</span>
          </div>
        </li>
        <li>
          <div class="d-flex justify-content-between">
            <span> UW Graded Attempted:</span>
            <span>{{ person.student.total_grade_attempted }}</span>
          </div>
        </li>
        <li>
          <div class="d-flex justify-content-between">
            <span>UW Graded Earned:</span>
            <span>xxx</span>
          </div>
        </li>
        <li>
          <div class="d-flex justify-content-between">
            <span>UW Graded Points:</span>
            <span>{{ person.student.total_grade_points }}</span>
          </div>
        </li>
        <li>
          <div class="d-flex justify-content-between">
            <span>UW GPA:</span>
            <span class="fw-bold">{{
              (person.student.total_grade_points /
              person.student.total_grade_attempted).toFixed(2)
            }}</span>
          </div>
        </li>
      </ul>
      <ul class="list-unstyled m-0">
        <li>
          <div class="d-flex justify-content-between">
            <span>UW Credits Earned:</span>
            <span>{{ person.student.total_uw_credits }}</span>
          </div>
        </li>
        <li>
          <div class="d-flex justify-content-between">
            <span>Extension Credits:</span>
            <span>{{ person.student.total_extension_credits }}</span>
          </div>
        </li>
        <li>
          <div class="d-flex justify-content-between">
            <span>Transfer Credits:</span>
            <span>{{ person.student.total_transfer_credits }}</span>
          </div>
        </li>
        <li><hr /></li>
        <li>
          <div class="d-flex justify-content-between">
            <span>Total Credits Earned</span>
            <span>{{ person.student.total_credits }}</span>
          </div>
        </li>
      </ul>
    </template>
  </axdd-card>
</template>

<script>
export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {},
};
</script>
