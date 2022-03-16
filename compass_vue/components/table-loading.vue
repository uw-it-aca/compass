<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col" style="width: 30%;">Name</th>
        <th scope="col" class="w-25">Student Number</th>
        <th scope="col">Priority</th>
        <th scope="col">Class</th>
        <th scope="col">Enroll Status</th>
        <th scope="col">Status</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="index in 3" :key="index">
        <td class="ps-0 placeholder-glow d-flex justify-content-start">
            <div class="me-2">
              <span class="placeholder d-inline-block rounded-circle bg-light-gray" style="width: 55px; height: 55px">&nbsp;</span>
            </div>
            <div class="w-100">
              <span class="placeholder bg-light-gray col-10"></span>
              <span class="placeholder bg-light-gray col-4"></span>
            </div>
        </td>
        <td class="placeholder-glow">
          <div><span class="placeholder bg-light-gray col-12"></span></div>
        </td>
        <td class="placeholder-glow">
          <div><span class="placeholder bg-light-gray col-9"></span></div>
        </td>
        <td class="placeholder-glow">
          <div><span class="placeholder bg-light-gray col-10"></span></div>
        </td>
        <td class="placeholder-glow">
          <div><span class="placeholder bg-light-gray col-7"></span></div>
        </td>
        <td class="placeholder-glow">
          <div><span class="placeholder bg-light-gray col-8"></span></div>
        </td>
      </tr>
    </tbody>
  </table>
</template>
