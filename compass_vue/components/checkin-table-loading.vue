<template>
  <div class="table-responsive m-n3">
    <table class="table mb-0">
      <thead class="small">
        <tr>
          <th class="ps-3 bg-body-tertiary" style="width: 33%" scope="col">
            Student
          </th>
          <th class="bg-body-tertiary" scope="col" style="width: 15%">
            Check-in Date
          </th>
          <th class="bg-body-tertiary" scope="col" style="width: 15%">
            Source
          </th>
          <th class="bg-body-tertiary" scope="col" style="width: 15%">
            Contact Type
          </th>
          <th class="bg-body-tertiary" scope="col" style="width: 15%">
            Meeting With
          </th>
          <th class="bg-body-tertiary text-nowrap" scope="col">
            Assigned Adviser
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
            <div><span class="placeholder bg-body-secondarycol-10"></span></div>
          </td>
          <td class="placeholder-glow">
            <div><span class="placeholder bg-body-secondary col-7"></span></div>
          </td>
          <td class="placeholder-glow">
            <div><span class="placeholder bg-body-secondary col-7"></span></div>
          </td>
          <td class="placeholder-glow">
            <div><span class="placeholder bg-body-secondary col-7"></span></div>
          </td>
          <td class="placeholder-glow">
            <div><span class="placeholder bg-body-secondary col-7"></span></div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
