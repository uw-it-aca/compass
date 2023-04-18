<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Contacts</axdd-card-heading>
      <axdd-card-action>
        <AddEditContact
          :button-type="'button'"
          :person="person"
          @contactUpdated="loadStudentContacts()"
          ><i class="bi bi-calendar-plus text-dark me-2"></i>Record new
          contact</AddEditContact
        >
      </axdd-card-action>
    </template>
    <template #body>
      <template v-if="contacts.length > 0">
        <div class="table-responsive m-n3">
          <table class="table m-0">
            <thead class="table-light text-muted small">
              <tr>
                <th class="ps-3">Date</th>
                <th>Details</th>
                <th>&nbsp;</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="contact in contacts" :key="contact.id">
                <td scope="row" class="ps-3" style="width: 25%">
                  <div>{{ formatDate(contact.checkin_date, "LLL") }}</div>
                  <div class="text-muted small">
                    <i class="bi bi-person-circle me-1"></i
                    >{{ contact.app_user.uwnetid }}
                  </div>
                </td>
                <td class="align-bottom">
                  <div
                    class="badge rounded-pill alert alert-dark-purple border-0 px-2 py-1 m-0 me-2"
                  >
                    {{ contact.contact_type.name }}
                  </div>

                  <div
                    class="badge rounded-pill alert alert-secondary border-0 px-2 py-1 m-0 me-1"
                  >
                    {{ contact.contact_method.name }}
                  </div>

                  <ul
                    v-if="contact.contact_topics"
                    class="list-unstyled mt-2 mb-0"
                  >
                    <li
                      v-for="topic in contact.contact_topics"
                      :key="topic.id"
                      class="badge rounded-pill alert alert-dark-beige border-0 px-2 py-1 mb-0 me-1"
                    >
                      {{ topic.name }}
                    </li>
                  </ul>

                  <div v-if="contact.notes" class="mt-3">
                    <span class="small text-muted visually-hidden">Notes</span>
                    <p class="text-dark small">
                      {{ contact.notes }}
                    </p>
                  </div>
                  <div
                    v-if="contact.actions"
                    class="border-top border-light pt-3"
                  >
                    <span class="small text-muted visually-hidden"
                      >Actions</span
                    >
                    <p class="text-muted small">
                      {{ contact.actions }}
                    </p>
                  </div>
                </td>
                <td class="p-3">
                  <AddEditContact
                    v-if="contact.app_user.uwnetid == userName"
                    :button-type="'link'"
                    :person="person"
                    :contact-id="contact.id"
                    @contactUpdated="loadStudentContacts()"
                    ><i class="bi bi-pencil text-dark me-2"></i>Edit
                    contact</AddEditContact
                  >
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
      <template v-else>
        <p>No contacts found</p>
      </template>
    </template>
  </axdd-card>
</template>

<script>
import dataMixin from "../../mixins/data_mixin.js";
import AddEditContact from "../add-contact.vue";
import { formatDate } from "../../utils/dates";

export default {
  mixins: [dataMixin],
  components: {
    AddEditContact,
  },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return {
      formatDate,
    };
  },
  data() {
    return {
      contacts: {},
      userName: document.body.getAttribute("data-user-netid"),
      userOverride: document.body.getAttribute("data-user-override"),
    };
  },
  created() {
    this.loadStudentContacts();
  },
  methods: {
    loadStudentContacts: function () {
      this.getStudentContacts(this.person.student.system_key).then(
        (response) => {
          if (response.data) {
            this.contacts = response.data;
          }
        }
      );
    },
  },
};
</script>

<style lang="scss">
tbody {
  td {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
  }
}
</style>
