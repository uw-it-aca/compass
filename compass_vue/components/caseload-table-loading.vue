<template>
  <div class="table-responsive m-n3">
    <table class="table mb-0">
      <thead class="text-muted small">
        <tr>
          <th scope="col" style="width: 33%" class="ps-3 bg-body-tertiary">
            Student
          </th>
          <th scope="col" style="width: 15%" class="bg-body-tertiary">Class</th>
          <th scope="col" class="bg-body-tertiary">Campus</th>
          <th
            scope="col"
            style="width: 33%"
            class="bg-body-tertiary text-nowrap"
          >
            Status
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="index in 3" :key="index">
          <td class="ps-3 placeholder-glow d-flex justify-content-start">
            <div class="me-2">
              <span
                class="placeholder d-inline-block rounded-circle bg-body-secondary"
                style="width: 55px; height: 55px"
                >&nbsp;</span
              >
            </div>
            <div class="w-100">
              <span class="placeholder bg-body-secondary col-10"></span>
              <span class="placeholder bg-body-secondary col-4"></span>
            </div>
          </td>
          <td class="placeholder-glow">
            <div>
              <span class="placeholder bg-body-secondary col-12"></span>
            </div>
          </td>
          <td class="placeholder-glow">
            <div>
              <span class="placeholder bg-body-secondary col-10"></span>
            </div>
          </td>
          <td class="placeholder-glow">
            <div>
              <span class="placeholder bg-body-secondary col-10"></span><br />
              <span class="placeholder bg-body-secondary col-4"></span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
