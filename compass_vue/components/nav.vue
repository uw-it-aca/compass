<template>
  <div class="text-white small">
    <ul class="nav flex-column">
      <li class="nav-item mb-1">
        <button
          class="btn btn-toggle align-items-center collapsed collapsed py-1 text-white bg-dark-purple w-100 text-start"
          data-bs-toggle="collapse"
          data-bs-target="#caseload-collapse"
          aria-expanded="false"
        >
          <i class="bi bi-briefcase-fill me-2"></i>Caseloads
        </button>
        <div class="collapse" id="caseload-collapse">
          <div class="p-3">
            <div class="mb-4">
              <div class="small lh-lg">Display caseload for:</div>
              <select
                class="form-select form-select-sm"
                aria-label="Default select example"
              >
                <option value="0">All advisers</option>
                <option selected value="1">Jon Average</option>
                <option value="2">April Foolery</option>
                <option value="3">Bob Samsonite</option>
              </select>
            </div>
            <div class="form-check">
              <input
                class="form-check-input"
                type="radio"
                name="flexRadioDefault"
                id="flexRadioDefault1"
                checked
              />
              <label class="form-check-label" for="flexRadioDefault1">Active</label>
            </div>
            <div class="form-check">
              <input
                class="form-check-input"
                type="radio"
                name="flexRadioDefault"
                id="flexRadioDefault2"
              />
              <label class="form-check-label" for="flexRadioDefault2">Inactive</label>
            </div>
          </div>
        </div>
      </li>
      <li class="nav-item mb-1">
        <button
          class="btn btn-toggle align-items-center collapsed collapsed py-1 text-white bg-dark-purple w-100 text-start"
          data-bs-toggle="collapse"
          data-bs-target="#retention-collapse"
          aria-expanded="false"
        >
          <i class="bi bi-activity me-2"></i>Retention Data
        </button>
        <div class="collapse" id="retention-collapse">
          <div class="p-3">
            <div class="fw-bold">Sign-ins</div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck1" />
              <label class="form-check-label" for="defaultCheck1">High</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck2" />
              <label class="form-check-label" for="defaultCheck2">Average</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck2" />
              <label class="form-check-label" for="defaultCheck2">Low</label>
            </div>

            <div class="fw-bold">Activity</div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck3" />
              <label class="form-check-label" for="defaultCheck3">High</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck4" />
              <label class="form-check-label" for="defaultCheck4">Average</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck5" />
              <label class="form-check-label" for="defaultCheck5">Low</label>
            </div>

            <div class="fw-bold">Assignments</div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck6" />
              <label class="form-check-label" for="defaultCheck6">High</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck7" />
              <label class="form-check-label" for="defaultCheck7">Average</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck8" />
              <label class="form-check-label" for="defaultCheck8">Low</label>
            </div>

            <div class="fw-bold">Grades</div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck9" />
              <label class="form-check-label" for="defaultCheck9">High</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck10" />
              <label class="form-check-label" for="defaultCheck10">Average</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck11" />
              <label class="form-check-label" for="defaultCheck11">Low</label>
            </div>

            <ul class="border-top mt-3 pt-3 mb-0 list-inline">
              <li class="list-inline-item">
                <strong>Low</strong> -5 to -3
              </li>
              <li class="list-inline-item">
                <strong>Average</strong> -2.9 to +2.9
              </li>
              <li class="list-inline-item">
                <strong>High</strong> +3 to +5
              </li>
            </ul>
          </div>
        </div>
      </li>
      <li class="nav-item mb-1">
        <button
          class="btn btn-toggle align-items-center collapsed collapsed py-1 text-white bg-dark-purple w-100 text-start"
          data-bs-toggle="collapse"
          data-bs-target="#populations-collapse"
          aria-expanded="false"
        >
          <i class="bi bi-people-fill me-2"></i>Populations
        </button>
        <div class="collapse" id="populations-collapse">
          <div class="p-3">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck12" />
              <label class="form-check-label" for="defaultCheck12">Pre-major</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck17" />
              <label class="form-check-label text-nowrap" for="defaultCheck17">Extended Pre-major</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck13" />
              <label class="form-check-label" for="defaultCheck13">STEM</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck14" />
              <label class="form-check-label" for="defaultCheck14">Freshman (credit)</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck20" />
              <label class="form-check-label" for="defaultCheck20">First-Year (at UW)</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck15" />
              <label class="form-check-label" for="defaultCheck15">Athlete</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck16" />
              <label class="form-check-label" for="defaultCheck16">International</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck17" />
              <label class="form-check-label" for="defaultCheck17">Graduate</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck18" />
              <label class="form-check-label" for="defaultCheck18">Running Start</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value id="defaultCheck19" />
              <label class="form-check-label" for="defaultCheck19">Transfer</label>
            </div>

            <div class="fw-bold">Sport</div>
            <select class="form-select form-select-sm" aria-label="Default select example">
              <option selected>All sports</option>
              <option value="1">Football</option>
              <option value="2">Soccer</option>
              <option value="3">Track</option>
            </select>
          </div>
        </div>
      </li>
    </ul>

    <button type="button" class="my-4 btn btn-sm btn-beige">Update results</button>
  </div>
</template>



<style lang="scss">
</style>
