<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Contacts (compass)</axdd-card-heading>
      <axdd-card-action>
        <AddEditContact
          :button-type="'button'"
          :person="person"
          @contactUpdated="loadStudentContacts()"
          ><i class="bi bi-plus-square-dotted me-2"></i>Record new
          contact</AddEditContact
        >
      </axdd-card-action>
    </template>
    <template #body>
      <template v-if="contacts.length > 0">
        <div class="table-responsive">
          <table class="table table-hover m-0">
            <thead class="small">
              <tr>
                <th style="width: 33%">Details</th>
                <th>Notes/Actions</th>
              </tr>
            </thead>
            <tbody class="table-group-divider">
              <tr v-for="contact in contacts" :key="contact.id">
                <td scope="row">
                  <p>
                    {{ contact.date }} {{ contact.time }}
                    {{ contact.contact_type.name }}<br />
                    {{ contact.author.uwnetid }} -
                    <AddEditContact
                      :button-type="'link'"
                      :person="person"
                      :contact-id="contact.id"
                      @contactUpdated="loadStudentContacts()"
                      >edit contact</AddEditContact
                    >
                  </p>
                  <div class="small">
                    Topics:
                    <span
                      v-for="(topic, index) in contact.contact_topics"
                      :key="topic.id"
                      >{{ topic.name }}
                      <span v-if="index + 1 < contact.contact_topics.length"
                        >,&nbsp;</span
                      >
                    </span>
                  </div>
                </td>
                <td>
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
