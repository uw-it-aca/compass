<template>
  <div class="card border-light-gray shadow-sm rounded-3 mb-4">
    <div class="card-header bg-white border-0 p-4 pb-0 d-flex justify-content-between">
      <h2
        class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
      >Contact</h2>
      <div>
        <AddContact><i class="bi bi-plus-square-dotted me-2"></i>Record new contact</AddContact>
      </div>
    </div>
    <div class="card-body p-4">
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
              <td scope="row">09/23/2020</td>
              <td>1:55PM</td>
              <td>Drop-in</td>
              <td>Jon Average</td>
              <td>
                <p>
                  <span class="badge bg-beige text-dark fw-normal">
                    <i class="bi bi-lock-fill"></i> Restricted
                  </span>
                  Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam, ducimus
                  mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis doloribus
                  expedita iure fuga obcaecati modi incidunt. Repellendus velit asperiores
                  dolores excepturi?
                </p>
                <p class="text-end small">
                  <AddContact>Edit contact</AddContact>
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
                  Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam, ducimus
                  mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis doloribus
                  expedita iure fuga obcaecati modi incidunt. Repellendus velit asperiores
                  dolores excepturi?
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
                  <span class="badge bg-beige text-dark fw-normal">
                    <i class="bi bi-lock-fill"></i> Restricted
                  </span> Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam, ducimus
                  mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis doloribus
                  expedita iure fuga obcaecati modi incidunt. Repellendus velit asperiores
                  dolores excepturi?
                </p>
                <p class="text-end small">
                  <AddContact>Edit contact</AddContact>
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
                  Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam, ducimus
                  mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis doloribus
                  expedita iure fuga obcaecati modi incidunt. Repellendus velit asperiores
                  dolores excepturi?
                </p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>


<script>
import AddContact from '../add-contact.vue';

export default {
  components: {
    AddContact
  },
  data() {
    return { };
  },
}

</script>
