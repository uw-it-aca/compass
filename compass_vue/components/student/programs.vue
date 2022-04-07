<template>
  <div class="card border-light-gray shadow-sm rounded-3 mb-4">
    <div class="card-header bg-white border-0 p-4 pb-0">
      <h2
        class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
      >Programs</h2>
    </div>
    <div class="card-body p-4">
      <p>UW Programs (from EDW?)</p>
      <ul>
        <li>Honor's</li>
        <li>Dean's List</li>
        <li>Athletics</li>
        <li>EOP</li>
      </ul>

      <hr />

      <p>OMAD Programs (if EOP yes)</p>
      <ul>
        <li>Pre-professional: yes/no</li>
        <li>IC Eligible: yes/no</li>
        <li>
          <template v-if="student.special_program_code">
            <b>yes</b>/no
          </template>
          <template v-else>CAMP, TRIO SSS, Champions</template>
        </li>
      </ul>
      <p>
        <a href="#" class="small">Edit Programs (ADMIN)</a>
      </p>
      <div class="border border-danger">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" value id="defaultCheck1" />
          <label class="form-check-label" for="defaultCheck1">CAMP</label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="checkbox" value id="defaultCheck2" />
          <label class="form-check-label" for="defaultCheck2">TRIO</label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="checkbox" value id="defaultCheck3" />
          <label class="form-check-label" for="defaultCheck3">SSS</label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="checkbox" value id="defaultCheck4" />
          <label class="form-check-label" for="defaultCheck4">Champions</label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="checkbox" value id="defaultCheck5" />
          <label class="form-check-label" for="defaultCheck5">IC Eligible</label>
        </div>
        <div class="text-end">
          <button
            type="button"
            class="btn btn-outline-dark-beige btn-sm rounded-pill"
          >Update programs</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    student: {
      type: Object,
      required: true,
    },
  },
  components: {
  },
  data() {
    return {};
  },
}
</script>
