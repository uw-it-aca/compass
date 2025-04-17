<template>
  <BCard
    class="shadow-sm rounded-3"
    header-class="p-3 d-flex align-items-center justify-content-between"
    header-bg-variant="transparent"
    footer-bg-variant="transparent"
  >
    <template #header>
      <div class="fs-6 fw-bold">Credit summary</div>
    </template>

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
            (
              person.student.total_grade_points /
              person.student.total_grade_attempted
            ).toFixed(2)
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
  </BCard>
</template>

<script>
import { BCard } from "bootstrap-vue-next";

export default {
  components: { BCard },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
};
</script>
