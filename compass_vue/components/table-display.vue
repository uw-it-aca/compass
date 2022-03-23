<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col" style="width: 325px;">Name</th>
        <th scope="col" style="width:155px;">Student Number</th>
        <th scope="col">Priority</th>
        <th scope="col">Class</th>
        <th scope="col">Enroll Status</th>
        <th scope="col">Status</th>
        <th scope="col">&nbsp;</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="index in 6" :key="index" >
        <td>
          <div class="d-flex">
            <div class="me-2" style="min-width: 55px">
              <div class="border-danger rounded-circle border border-3">
                <img
                  src="https://randomuser.me/api/portraits/thumb/men/4.jpg"
                  class="img-fluid rounded-circle border border-white border-2"
                />
              </div>
            </div>
            <div class="flex-fill">
              <div class="text-nowrap">
                <span>Pals, Hue</span
                ><span class="badge rounded-pill border border-muted text-dark small">M</span
                ><span class="badge rounded-pill border border-muted text-dark small"
                  ><i class="bi bi-trophy-fill text-purple"></i
                ></span>
              </div>
              <div class="small text-secondary">hp396</div>
            </div>
          </div>
        </td>
        <td>
          <router-link :to="{ path: '/student/1544522' }">1544522</router-link>
        </td>
        <td>top/middle/bottom</td>
        <td>1st Year Professional</td>
        <td>Enrolled</td>
        <td>Active</td>
        <td class="pe-0 align-middle text-end">
          <add-contact></add-contact>
        </td>
      </tr>
    </tbody>
  </table>
</template>


<script>
import AddContact from '../components/add-contact.vue';

export default {
  components: {
    'add-contact': AddContact,
  },
  data() {
    return { }
  }
};
</script>
