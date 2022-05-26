<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col" style="width: 325px">Name</th>
        <th scope="col" style="width: 155px">Student Number</th>
        <th scope="col">Class</th>
        <th scope="col">Enrollment Status</th>
        <th scope="col">&nbsp;</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="person in persons" :key="person.id">
        <td>
          <div class="d-flex">
            <div class="me-2" style="min-width: 55px">
              <div class="border-danger rounded-circle border border-3">
                <img
                  v-if="person.student.gender === 'M'"
                  src="https://randomuser.me/api/portraits/thumb/men/1.jpg"
                  class="img-fluid rounded-circle border border-white border-2"
                />
                <img
                  v-else
                  src="https://randomuser.me/api/portraits/thumb/women/1.jpg"
                  class="img-fluid rounded-circle border border-white border-2"
                />
              </div>
            </div>
            <div class="flex-fill">
              <div class="text-nowrap">
                <span>{{ person.display_name }}</span
                ><span
                  v-if="person.student.gender === 'M'"
                  class="badge rounded-pill border border-muted text-dark small"
                  >M</span
                >
                <span
                  v-if="person.student.gender === 'F'"
                  class="badge rounded-pill border border-muted text-dark small"
                  >F</span
                ><span
                  v-if="person.student.sports.length > 0"
                  class="badge rounded-pill border border-muted text-dark small"
                  ><i class="bi bi-trophy-fill text-purple"></i
                ></span>
              </div>
              <div class="small text-secondary">
                <router-link :to="{ path: '/student/' + person.uwnetid }">
                  {{ person.uwnetid }}
                </router-link>
              </div>
            </div>
          </div>
        </td>
        <td>
          <router-link :to="{ path: '/student/' + person.uwnetid }">
            {{ person.student.student_number }}
          </router-link>
        </td>
        <td>{{ person.student.class_desc }}</td>
        <td>
          <template v-if="person.student.registered_in_quarter">
            Registered
          </template>
          <template v-else> Unregistered </template>
        </td>
        <td class="align-middle text-end">
          <div class="small text-danger">You have not added a note yet!</div>
          <add-contact
            ><i class="bi bi-plus-square-dotted me-2"></i>Update Contact</add-contact
          >
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import AddContact from "../components/add-contact.vue";

export default {
  components: {
    "add-contact": AddContact,
  },
  props: {
    persons: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
};
</script>
