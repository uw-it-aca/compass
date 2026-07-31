<!-- Copyright 2026 UW-IT, University of Washington -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

<template>
  <div>
    <h1>OMAD Contact Processing Queue</h1>
    <table class="table table-striped">
      <colgroup>
        <col style="width: auto" />
        <col style="width: auto" />
        <col style="width: auto" />
        <col style="width: auto" />
        <col style="width: auto" />
        <col style="width: 60%" />
      </colgroup>
      <thead>
        <tr>
          <th>ID</th>
          <th>Created</th>
          <th>Processing Attempts</th>
          <th>Last Attempted</th>
          <th>Last Error</th>
          <th>Contact JSON</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td colspan="6" class="text-center">Loading queue...</td>
        </tr>
        <tr v-if="error && !loading">
          <td colspan="6" class="text-danger">{{ error }}</td>
        </tr>
        <tr v-for="contact in displayContacts" :key="contact.id">
          <td>{{ contact.id }}</td>
          <td>{{ contact.created }}</td>
          <td>{{ contact.processing_attempts }}</td>
          <td>{{ contact.process_attempted_date }}</td>
          <td>{{ contact.processing_error }}</td>
          <td>
            {{ contact.json }}
            <details v-if="contact.stack_trace">
              <summary>Show traceback</summary>
              <pre>{{ contact.stack_trace }}</pre>
            </details>
          </td>
        </tr>
        <tr v-if="!loading && !error && displayContacts.length === 0">
          <td colspan="6" class="text-center">No contacts in queue.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "OMADContactAdmin",
  props: {
    tool: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      queueContacts: [],
      loading: false,
      error: "",
    };
  },
  computed: {
    displayContacts() {
      return this.queueContacts;
    },
  },
  async mounted() {
    await this.loadContacts();
  },
  methods: {
    async loadContacts() {
      this.loading = true;
      this.error = "";
      try {
        const response = await fetch("/api/internal/support/omad_contact_queue/", {
          credentials: "same-origin",
        });
        if (!response.ok) {
          throw new Error("Unable to load OMAD contact queue");
        }
        const rows = await response.json();
        this.queueContacts = Array.isArray(rows) ? rows : [];
      } catch (err) {
        this.error = String(err);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
table {
  border-collapse: collapse;
  table-layout: fixed;
  width: 100%;
}

th,
td {
  text-align: left;
  padding: 8px;
}

details {
  border: 1px solid #aaa;
  border-radius: 4px;
  padding: 0.5em 0.5em 0;
}

summary {
  font-weight: bold;
  margin: -0.5em -0.5em 0;
  padding: 0.5em;
  cursor: pointer;
}

details[open] {
  padding: 0.5em;
}

details[open] summary {
  border-bottom: 1px solid #aaa;
  margin-bottom: 0.5em;
}
</style>
