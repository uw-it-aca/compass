<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2"
        >Instruction Center Visits</axdd-card-heading
      >
    </template>
    <template #body>
      <div class="d-flex">
        <div class="vr text-purple" aria-hidden="true"></div>
        <ul class="list-unstyled mb-0" style="margin-left: -6px; z-index: 1">
          <li class="d-flex mb-2">
            <i class="bi bi-circle-fill text-purple fs-10 mt-1 me-2"></i>
            <span
              >09/23/2020, BUS 220 <br />
              10:35am - 11:42am</span
            >
          </li>
          <li class="d-flex mb-2">
            <i class="bi bi-circle-fill text-purple fs-10 mt-1 me-2"></i>
            <span>09/23/2020, CSE 143<br />10:35am - 11:42am</span>
          </li>
          <li class="d-flex mb-2">
            <i class="bi bi-circle-fill text-purple fs-10 mt-1 me-2"></i>
            <span>09/23/2020, CSE 143<br />10:35am - 11:42am</span>
          </li>
          <li class="d-flex mb-2">
            <i class="bi bi-circle-fill text-purple fs-10 mt-1 me-2"></i>
            <span>09/23/2020, CSE 143<br />10:35am - 11:42am</span>
          </li>
          <li class="d-flex">
            <i class="bi bi-circle-fill text-purple fs-10 mt-1 me-2"></i>
            <span>09/23/2020, CSE 143<br />10:35am - 11:42am</span>
          </li>
        </ul>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import { Card, CardHeading } from "axdd-components";

export default {
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
  },
};
</script>
