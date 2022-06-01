<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Contacts (compass)</axdd-card-heading>
      <axdd-card-action>
        <AddContact class="btn btn-sm btn-outline-dark-beige"
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
              <th style="width: 33%">Details</th>
              <th>Notes/Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td scope="row">
                <p>
                  05/26/2022 2:30PM Appointment<br />
                  You - <a href="#">edit contact</a>
                </p>
                <div class="small">topics: asdflk, asdlfj, lajsdf, asdlfkj</div>
              </td>
              <td>
                <p class="text-muted">notes: No notes entered!</p>
                <p class="text-muted">action: no actions</p>
              </td>
            </tr>
            <tr>
              <td scope="row">
                <p>
                  09/23/2020 1:55PM Drop-in<br />
                  You - <a href="#">edit contact</a>
                </p>
                <div class="small">topics: asdflk, asdlfj, lajsdf, asdlfkj</div>
              </td>
              <td>
                <p>
                  notes: Lorem ipsum dolor sit amet consectetur adipisicing
                  elit. Totam, ducimus mollitia! Maiores suscipit tempore sunt,
                  ipsa beatae omnis doloribus expedita iure fuga obcaecati modi
                  incidunt. Repellendus velit asperiores dolores excepturi?
                </p>
                <p>action: student needs to do this</p>
              </td>
            </tr>
            <tr>
              <td scope="row">
                <p>
                  07/04/2020 10:52AM Quick Question<br />
                  Boris Washington
                </p>
                <div class="small">topics: asdflk, asdlfj, lajsdf, asdlfkj</div>
              </td>
              <td>
                <p>
                  notes: Lorem ipsum dolor sit amet consectetur adipisicing
                  elit. Totam, ducimus mollitia! Maiores suscipit tempore sunt,
                  ipsa beatae omnis doloribus expedita iure fuga obcaecati modi
                  incidunt. Repellendus velit asperiores dolores excepturi?
                </p>
                <p>action: student needs to do this</p>
              </td>
            </tr>
            <tr>
              <td scope="row">
                <p>
                  06/29/2020 3:15PM Appointment<br />
                  You - <a href="#">edit contact</a>
                </p>
                <div class="small">topics: asdflk, asdlfj, lajsdf, asdlfkj</div>
              </td>
              <td>
                <p>
                  notes: Lorem ipsum dolor sit amet consectetur adipisicing
                  elit. Totam, ducimus mollitia! Maiores suscipit tempore sunt,
                  ipsa beatae omnis doloribus expedita iure fuga obcaecati modi
                  incidunt. Repellendus velit asperiores dolores excepturi?
                </p>
                <p>action: student needs to do this</p>
              </td>
            </tr>
            <tr>
              <td scope="row">
                <p>
                  5/14/2020 2:15PM Telephone<br />
                  Otto Wilson
                </p>
                <div class="small">topics: asdflk, asdlfj, lajsdf, asdlfkj</div>
              </td>
              <td>
                <p>
                  notes: Lorem ipsum dolor sit amet consectetur adipisicing
                  elit. Totam, ducimus mollitia! Maiores suscipit tempore sunt,
                  ipsa beatae omnis doloribus expedita iure fuga obcaecati modi
                  incidunt. Repellendus velit asperiores dolores excepturi?
                </p>
                <p>action: student needs to do this</p>
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
