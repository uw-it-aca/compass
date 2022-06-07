<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Visits (compass)</axdd-card-heading>
    </template>
    <template #body>
      <div class="table-responsive">
        <table class="table table-hover table-striped m-0">
          <thead class="small">
            <tr>
              <th>Date</th>
              <th>Course</th>
              <th>Check-in</th>
              <th>Check-out</th>
              <th>Duration</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td scope="row">09/23/2020</td>
              <td>BUS 220</td>
              <td>10:35am</td>
              <td>11:42pm</td>
              <td>1hr 2mins</td>
            </tr>
            <tr>
              <td scope="row">07/04/2020</td>
              <td>CSE 142</td>
              <td>9:15am</td>
              <td>11:2am</td>
              <td>2 hrs</td>
            </tr>
            <tr>
              <td scope="row">06/29/2020</td>
              <td>BUS 220</td>
              <td>4:31pm</td>
              <td>4:45pm</td>
              <td>15 mins</td>
            </tr>
            <tr>
              <td scope="row">5/14/2020</td>
              <td>BUS 220</td>
              <td>2:34pm</td>
              <td>6:35pm</td>
              <td>4 hrs</td>
            </tr>
          </tbody>
        </table>
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
