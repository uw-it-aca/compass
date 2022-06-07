<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Contacts (compass)</axdd-card-heading>
      <axdd-card-action>
        <AddEditContact :button-type="'button'"
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
                  {{ contact.pub_date }} {{ contact.time }}
                  {{ contact.contact_type.name }}<br />
                  You -
                  <AddEditContact :button-type="'link'"
                    >edit contact</AddEditContact
                  >
                </p>
                <div class="small">
                  topics:
                  <span
                    v-for="topic in contact.contact_topics"
                    :key="topic.id"
                    >{{ topic.name }}</span
                  >
                </div>
              </td>
              <td>
                <p class="text-muted">notes: No notes entered!</p>
                <p class="text-muted">action: no actions</p>
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
  props: ["contacts"],
  data() {
    return {};
  },
};
</script>
