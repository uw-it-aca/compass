<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Contacts</axdd-card-heading>
      <axdd-card-action>
        <AddEditContact
          :button-type="'button'"
          :person="person"
          @contactUpdated="loadStudentContacts()"
          ><i class="bi bi-plus-square text-white me-2"></i>Record new
          contact</AddEditContact
        >
      </axdd-card-action>
    </template>
    <template #body>
      <template v-if="contacts.length > 0">
        <div class="table-responsive m-n3">
          <table class="table table-striped table-borderless m-0 small">
            <thead class="">
              <tr>
                <th class="ps-3">Date</th>
                <th>Type</th>
                <th>Details</th>
              </tr>
            </thead>
            <tbody class="">
              <tr v-for="contact in contacts" :key="contact.id">
                <td scope="row" class="ps-3" style="width: 25%">
                  <p>
                    {{ contact.date }} {{ contact.time }}
                    <br />
                    {{ contact.author.uwnetid }} -
                    <AddEditContact
                      :button-type="'link'"
                      :person="person"
                      :contact-id="contact.id"
                      @contactUpdated="loadStudentContacts()"
                      >edit contact</AddEditContact
                    >
                  </p>
                </td>
                <td>
                  <span
                    class="badge rounded-pill alert alert-dark-purple border-0 px-2 py-1 me-1"
                    >{{ contact.contact_type.name }}</span
                  >
                </td>
                <td>
                  <div>
                    <span
                      v-for="topic in contact.contact_topics"
                      :key="topic.id"
                      class="badge rounded-pill alert alert-success border-0 px-2 py-1 me-1"
                      >{{ topic.name }}
                    </span>
                  </div>
                  <p class="text-muted">notes: {{ contact.notes }}</p>
                  <p class="text-muted">actions: {{ contact.actions }}</p>
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
import { Card, CardHeading, CardAction } from "axdd-components";
import AddEditContact from "../add-contact.vue";

export default {
  mixins: [dataMixin],
  components: {
    AddEditContact,
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-card-action": CardAction,
  },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      contacts: {},
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
