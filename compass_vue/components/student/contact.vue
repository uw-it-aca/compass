<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Contact</axdd-card-heading>
      <axdd-card-action>
        <AddContact
          ><i class="bi bi-plus-square-dotted me-2"></i>Record new
          contact</AddContact
        >
      </axdd-card-action>
    </template>
    <template #body>
      <div class="table-responsive">
        <table class="table m-0">
          <thead class="small">
            <tr>
              <th>Date</th>
              <th>Time</th>
              <th class="text-nowrap">Contact Type</th>
              <th>Staff</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
             <tr>
              <td scope="row">05/26/2022</td>
              <td>2:30PM</td>
              <td>Appointment</td>
              <td>Jon Average</td>
              <td>
                <p class="text-danger">No notes entered!</p>
                <p class="text-end small">
                  <a href="#">Edit contact</a>
                </p>
              </td>
            </tr>
            <tr>
              <td scope="row">09/23/2020</td>
              <td>1:55PM</td>
              <td>Drop-in</td>
              <td>Jon Average</td>
              <td>
                <p>
                  <span class="badge bg-beige text-dark fw-normal">
                    <i class="bi bi-people-fill"></i> Public
                  </span>
                  Lorem ipsum dolor sit amet consectetur adipisicing elit.
                  Totam, ducimus mollitia! Maiores suscipit tempore sunt, ipsa
                  beatae omnis doloribus expedita iure fuga obcaecati modi
                  incidunt. Repellendus velit asperiores dolores excepturi?
                </p>
                <p class="text-end small">
                  <a href="#">Edit contact</a>
                </p>
              </td>
            </tr>
            <tr>
              <td scope="row">07/04/2020</td>
              <td>10:52AM</td>
              <td>Quick Question</td>
              <td>Boris Washington</td>
              <td>
                <p>
                  Lorem ipsum dolor sit amet consectetur adipisicing elit.
                  Totam, ducimus mollitia! Maiores suscipit tempore sunt, ipsa
                  beatae omnis doloribus expedita iure fuga obcaecati modi
                  incidunt. Repellendus velit asperiores dolores excepturi?
                </p>
              </td>
            </tr>
            <tr>
              <td scope="row">06/29/2020</td>
              <td>3:15PM</td>
              <td>Appointment</td>
              <td>Jon Average</td>
              <td>
                <p>
                  Lorem ipsum dolor sit amet consectetur adipisicing elit.
                  Totam, ducimus mollitia! Maiores suscipit tempore sunt, ipsa
                  beatae omnis doloribus expedita iure fuga obcaecati modi
                  incidunt. Repellendus velit asperiores dolores excepturi?
                </p>
                <p class="text-end small">
                  <a href="#">Edit contact</a>
                </p>
              </td>
            </tr>
            <tr>
              <td scope="row">5/14/2020</td>
              <td>2:15PM</td>
              <td>Telephone</td>
              <td>Otto Wilson</td>
              <td>
                <p>
                  Lorem ipsum dolor sit amet consectetur adipisicing elit.
                  Totam, ducimus mollitia! Maiores suscipit tempore sunt, ipsa
                  beatae omnis doloribus expedita iure fuga obcaecati modi
                  incidunt. Repellendus velit asperiores dolores excepturi?
                </p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import { Card, CardHeading, CardAction } from "axdd-components";
import AddContact from "../add-contact.vue";

export default {
  components: {
    AddContact,
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-card-action": CardAction,
  },
  data() {
    return {};
  },
};
</script>
