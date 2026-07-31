<!-- Copyright 2026 UW-IT, University of Washington -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

<template>
  <div>
    <h1>Retention Analytics Data Admin</h1>

    <!-- ── Canvas Analytics Data ─────────────────────────────────────── -->
    <h2>Canvas Analytics Data</h2>
    <p>Compass jobs that fetch data from the Canvas Analytics GCS Bucket</p>
    <p>
      Runs weekly at 20:00 Sunday PST (04:00 Monday UTC), imports most recent
      week in bucket if it has not been imported already
    </p>
    <p>
      <strong>Reload:</strong> Removes the selected week's data from Compass and
      attempts to re-import from Canvas Analytics
    </p>
    <p>
      <strong>Delete:</strong> Removes the selected week's data from Compass; if
      most recent week is deleted, alert status will need to be re-calculated
    </p>
    <p>
      <em>
        Both of these actions have user facing impacts — if 'good' data is
        removed and not replaced users will be missing data
      </em>
    </p>

    <div v-if="actionMessage" :class="['alert', actionError ? 'alert-danger' : 'alert-success']">
      {{ actionMessage }}
    </div>
    <div v-if="loadError" class="alert alert-danger">{{ loadError }}</div>
    <p v-if="loading">Loading retention admin data...</p>

    <table class="table nowrap">
      <thead>
        <tr>
          <th>Import ID</th>
          <th>Year</th>
          <th>Quarter</th>
          <th>Week</th>
          <th>Import Date</th>
          <th>Last Processed</th>
          <th>Status</th>
          <th>Students With Scores</th>
          <th>Canvas Scores</th>
          <th>Signin Scores</th>
          <th>Predictions Filename</th>
          <th>Reload</th>
          <th>Delete</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="imp in viewData.imports" :key="imp.id">
          <td>{{ imp.id }}</td>
          <td>{{ imp.year }}</td>
          <td>{{ imp.quarter }}</td>
          <td>{{ imp.week }}</td>
          <td>{{ imp.created_date }}</td>
          <td>{{ imp.processed_date }}</td>
          <td>{{ imp.import_status }}</td>
          <td>{{ imp.student_count }}</td>
          <td>{{ imp.total_scores }}</td>
          <td>{{ imp.signin_scores }}</td>
          <td>{{ imp.prediction_filename }}</td>
          <td>
            <button
              v-if="imp.prediction_filename"
              class="btn btn-default btn-sm"
              :disabled="busy[`reload-${imp.id}`]"
              @click="reloadImport(imp.id)"
            >
              {{ busy[`reload-${imp.id}`] ? 'Reloading…' : 'Reload' }}
            </button>
            <span v-else>Cannot reload legacy weeks</span>
          </td>
          <td>
            <button
              class="btn btn-default btn-sm"
              :disabled="busy[`delete-${imp.id}`]"
              @click="deleteImport(imp.id)"
            >
              {{ busy[`delete-${imp.id}`] ? 'Deleting…' : 'Delete' }}
            </button>
          </td>
        </tr>
        <tr v-if="viewData.imports.length === 0">
          <td colspan="13">No imports found.</td>
        </tr>
      </tbody>
    </table>

    <!-- ── Student Alert Status ───────────────────────────────────────── -->
    <h2>Student Alert Status</h2>
    <p>
      Calculates student alert status (colored rings) from per-course
      predictions, uses the most recently imported week
    </p>
    <p>
      This is automatically run when data is loaded/reloaded and always builds
      alerts from the most recent analytics data in Compass
    </p>
    <p>
      <strong>Current alerts generated from week: </strong>
      <span v-if="viewData.alert_data.source_week">
        {{ viewData.alert_data.source_week.year }}-{{
          viewData.alert_data.source_week.quarter
        }}-week-{{ viewData.alert_data.source_week.week }}
      </span>
      <span v-else>No alerts calculated yet</span>
    </p>

    <button
      v-if="viewData.alert_data.current_week"
      class="btn btn-default"
      :disabled="busy['reload-alerts']"
      @click="reloadAlerts"
    >
      {{
        busy["reload-alerts"]
          ? "Calculating…"
          : `Calculate alerts from ${viewData.alert_data.current_week.year}-${viewData.alert_data.current_week.quarter}-week-${viewData.alert_data.current_week.week}`
      }}
    </button>
    <p>
      <em>
        Manually running this should rarely be needed, only if the current week
        was deleted or a transient error prevented automatic alert generation
      </em>
    </p>

    <table v-if="viewData.alert_data.source_week" class="table">
      <thead>
        <tr>
          <th>Students With Alert</th>
          <th>Total Success</th>
          <th>Total Warning</th>
          <th>Total Failure</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{ viewData.alert_data.total_alerts }}</td>
          <td>{{ viewData.alert_data.total_success }}</td>
          <td>{{ viewData.alert_data.total_warning }}</td>
          <td>{{ viewData.alert_data.total_danger }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>No prediction data loaded.</p>

    <!-- ── Canvas Analytics Files ─────────────────────────────────────── -->
    <h2>Canvas Analytics Files</h2>
    <p>List of files in Canvas Analytics GCS bucket</p>
    <p>
      Generated weekly by Canvas Analytics project at 06:00 Sunday PST
      (14:00 Sunday UTC)
    </p>
    <p>
      <strong>Associated Import ID:</strong> The Compass Import ID for the file;
      "Not Imported" if data not in Compass
    </p>
    <p>
      <strong>Reload:</strong> Will attempt to load or reload the specified data
      file in Compass
    </p>

    <template v-if="viewData.file_data !== null">
      <table class="table nowrap">
        <thead>
          <tr>
            <th>File Name</th>
            <th>Associated Import ID</th>
            <th>Reload</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="file in viewData.file_data" :key="file.week_key">
            <td>{{ file.filename }}</td>
            <td>{{ file.import_id }}</td>
            <td>
              <button
                class="btn btn-default btn-sm"
                :disabled="busy[`file-${file.week_string}`]"
                @click="loadFromFile(file.week_string)"
              >
                {{
                  busy[`file-${file.week_string}`] ? "Loading…" : "Reload"
                }}
              </button>
            </td>
          </tr>
          <tr v-if="viewData.file_data.length === 0">
            <td colspan="3">No files found.</td>
          </tr>
        </tbody>
      </table>
    </template>
    <p v-else>Cannot load files list from GCS bucket.</p>

    <!-- ── Prediction Files ───────────────────────────────────────────── -->
    <h2>Prediction Files</h2>
    <p>List of prediction files generated by Compass retention analytics jobs</p>

    <template v-if="viewData.prediction_files !== null && viewData.prediction_files.length > 0">
      <table class="table nowrap">
        <thead>
          <tr>
            <th>File Name</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="file in viewData.prediction_files" :key="file.filename">
            <td>{{ file.filename }}</td>
          </tr>
        </tbody>
      </table>
    </template>
    <p v-else>No prediction files found.</p>
  </div>
</template>

<script>
function getCsrfToken() {
  const name = "csrftoken=";
  for (const cookie of document.cookie.split(";")) {
    const c = cookie.trim();
    if (c.startsWith(name)) return decodeURIComponent(c.slice(name.length));
  }
  return null;
}

async function apiPut(url) {
  const resp = await fetch(url, {
    method: "PUT",
    headers: { "X-CSRFToken": getCsrfToken() },
  });
  if (!resp.ok) throw new Error(`${resp.status} ${resp.statusText}`);
  return resp.json();
}

async function apiDelete(url) {
  const resp = await fetch(url, {
    method: "DELETE",
    headers: { "X-CSRFToken": getCsrfToken() },
  });
  if (!resp.ok) throw new Error(`${resp.status} ${resp.statusText}`);
  return resp.json();
}

export default {
  name: "RetentionAdmin",
  props: {
    tool: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      viewData: this.normalizePageData({}),
      busy: {},
      actionMessage: null,
      actionError: false,
      loading: false,
      loadError: "",
    };
  },
  async mounted() {
    await this.loadPageData();
  },
  methods: {
    normalizePageData(data) {
      const base = data && typeof data === "object" ? data : {};
      return {
        imports: Array.isArray(base.imports) ? base.imports : [],
        alert_data: base.alert_data || {},
        file_data:
          base.file_data === null || Array.isArray(base.file_data)
            ? base.file_data
            : [],
        prediction_files:
          base.prediction_files === null || Array.isArray(base.prediction_files)
            ? base.prediction_files
            : [],
      };
    },
    async loadPageData() {
      this.loading = true;
      this.loadError = "";
      try {
        const response = await fetch(
          "/api/internal/support/retention_admin/page_data/",
          { credentials: "same-origin" }
        );
        if (!response.ok) {
          throw new Error("Unable to load retention admin data");
        }
        const data = await response.json();
        this.viewData = this.normalizePageData(data);
      } catch (err) {
        this.loadError = String(err);
      } finally {
        this.loading = false;
      }
    },
    setBusy(key, val) {
      this.busy = { ...this.busy, [key]: val };
    },
    async withBusy(key, fn) {
      this.setBusy(key, true);
      this.actionMessage = null;
      this.actionError = false;
      try {
        const result = await fn();
        this.actionMessage = result.message || "Done.";
        await this.loadPageData();
      } catch (err) {
        this.actionError = true;
        this.actionMessage = `Error: ${err.message}`;
      } finally {
        this.setBusy(key, false);
      }
    },
    reloadImport(importId) {
      this.withBusy(`reload-${importId}`, () =>
        apiPut(`/api/internal/support/retention_admin/manage/${importId}/`)
      );
    },
    deleteImport(importId) {
      this.withBusy(`delete-${importId}`, () =>
        apiDelete(`/api/internal/support/retention_admin/manage/${importId}/`)
      );
    },
    reloadAlerts() {
      this.withBusy("reload-alerts", () =>
        apiPut("/api/internal/support/retention_admin/reload_alerts/")
      );
    },
    loadFromFile(weekString) {
      this.withBusy(`file-${weekString}`, () =>
        apiPut(
          `/api/internal/support/retention_admin/file/${weekString}/`
        )
      );
    },
  },
};
</script>
