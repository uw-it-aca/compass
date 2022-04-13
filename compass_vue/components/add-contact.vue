<template>
  <a
    href="#"
    role="button"
    data-bs-toggle="modal"
    data-bs-target="#exampleModal"
    class="btn btn-sm btn-outline-dark-beige text-nowrap"
    ><slot>Add Contact</slot></a
  >

  <!-- contact modal -->
  <div
    class="modal fade text-start"
    id="exampleModal"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Record a contact</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="row mb-3">
            <div class="col">
              <label for="date" class="form-label">Date:</label>
              <input type="date" id="date" class="form-control" />
            </div>
            <div class="col">
              <label class="form-label">Contact type:</label>
              <select class="form-select" aria-label="Default select example">
                <option selected disabled>Choose one...</option>
                <option value="1">Quick Question</option>
                <option value="2">Appointment</option>
                <option value="3">Drop-in</option>
                <option value="4">Telephone</option>
              </select>
            </div>
            <div class="col">
              <div class="row">
                <div class="col">
                  <label for="appt-time" class="form-label">Check in time:</label>
                  <input
                    id="appt-time"
                    type="time"
                    name="appt-time"
                    value="13:30"
                    class="form-control"
                  />
                </div>

                <div class="col">
                  <label class="form-label">Duration:</label>
                  <select class="form-select" aria-label="Default select example">
                    <option selected>15</option>
                    <option value="1">30</option>
                    <option value="2">60</option>
                    <option value="3">90</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Topics Covered:</label>
            <div style="column-count: 3">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value id="flexCheck1" />
                <label class="form-check-label" for="flexCheck1">Add/Drop Class</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value id="flexCheck2" />
                <label class="form-check-label" for="flexCheck2">Join/Affiliate</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value id="flexCheck3" />
                <label class="form-check-label" for="flexCheck3">Academic Difficulties</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value id="flexCheck4" />
                <label class="form-check-label" for="flexCheck4">Hardship Withdrawl</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value id="flexCheck5" />
                <label class="form-check-label" for="flexCheck5">Internships</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value id="flexCheck6" />
                <label class="form-check-label" for="flexCheck6">Research Opportunities</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value id="flexCheck7" />
                <label class="form-check-label" for="flexCheck7"
                  >Graduate Professional School</label
                >
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" value id="flexCheck8" />
                <label class="form-check-label" for="flexCheck8">Testing/Assessment</label>
              </div>
            </div>
          </div>
          <div class="mb-3">
            <label for="exampleFormControlTextarea1" class="form-label">Notes</label>
            <textarea class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
          </div>

          <div class="mb-3">
            <label for="exampleFormControlTextarea2" class="form-label"
              >Actions and Recommmendations</label
            >
            <textarea class="form-control" id="exampleFormControlTextarea2" rows="3"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Save contact</button>
        </div>
      </div>
    </div>
  </div>
  <!-- end visit modal -->
</template>
