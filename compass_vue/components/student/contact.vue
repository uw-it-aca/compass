<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Contacts (compass)</axdd-card-heading>
      <axdd-card-action>
        <AddEditContact :button-type="'button'" :person="person"
          ><i class="bi bi-plus-square-dotted me-2"></i>Record new
          contact</AddEditContact
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
            <tr v-for="contact in contacts" :key="contact.id">
              <td scope="row">
                <p>
                  {{ contact.date }} {{ contact.time }}
                  {{ contact.contact_type.name }}<br />
                  {{ contact.author.uwnetid }} -
                  <AddEditContact
                    :button-type="'link'"
                    :person="person"
                    :contact="contact"
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
  </axdd-card>
</template>

<script>
import { Card, CardHeading, CardAction } from "axdd-components";
import AddEditContact from "../add-contact.vue";

export default {
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
    contacts: {
      type: Object,
      required: true,
      default: function () {
        return {};
      },
    },
  },
  data() {
    return {};
  },
};
</script>
