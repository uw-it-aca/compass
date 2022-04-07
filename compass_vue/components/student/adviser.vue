<template>
  <div class="card border-light-gray shadow-sm rounded-3 mb-4">
    <div class="card-header bg-white border-0 p-4 pb-0">
      <h2
        class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
      >Adviser</h2>
    </div>
    <div class="card-body p-4">
      <ul class="list-unstyled">
        <li class="fw-bold">John Average</li>
        <li>he/him</li>
        <li>Email</li>
        <li>Phone</li>
        <li class="border-top mt-2 pt-2">Dept Name: OMAD</li>
        <li>Campus location: MGH 123</li>
        <li>
          <a href="#" class="small">Edit adviser (ADMIN)</a>
        </li>
      </ul>

      <div class="border border-danger">
        <ul class="list-unstyled text-muted">
          <li>
            <p>This student does not have an assigned adviser.</p>
          </li>
          <li>
            <select class="form-select form-select-sm mb-2" aria-label=".form-select-sm example">
              <option selected>Select adviser</option>
              <option value="1">Bob</option>
              <option value="2">Tim</option>
              <option value="3">Joe</option>
            </select>
          </li>
          <li class="text-end">
            <button
              type="button"
              class="btn btn-outline-dark-beige btn-sm"
            >Update adviser</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>

</script>
