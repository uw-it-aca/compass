// about.vue

<template>
  <layout v-if="student.student_name !== undefined" :page-title="student.student_name">
    <template #title>
      <h1 v-if="$route.params.id" class="visually-hidden">{{ student.student_name }}</h1>
      <h1 v-else>Student</h1>
    </template>
    <template #content>
      <div v-if="$route.params.id">
        <div class="row my-4">
          <div class="col">
            <div class="bg-gray p-4 rounded-3">
              <div class="row">
                <div class="col-lg-6 pe-4 d-flex small">
                  <div>
                    <div
                      :class="priorityRing"
                      class="rounded-circle border border-4"
                      style="width: 140px"
                    >
                      <img
                        v-if="student.gender === 'F'"
                        :src="'https://randomuser.me/api/portraits/women/' + student.id + '.jpg'"
                        class="img-fluid rounded-circle border border-light border-3"
                      />
                      <img
                        v-else
                        :src="'https://randomuser.me/api/portraits/men/' + student.id + '.jpg'"
                        class="img-fluid rounded-circle border border-light border-3"
                      />
                    </div>
                    <div class="text-center mb-4">
                      <span class="fw-bold">Priority {{ student.retention.priority }}</span>
                    </div>
                  </div>
                  <div class="flex-fill ps-4 mb-4">
                    <div class="h3 text-dark axdd-font-encode-sans">
                      {{ student.student_preferred_last_name }},
                      {{ student.student_preferred_first_name }}
                    </div>
                    <div class="h5">
                      {{ $route.params.id }}, <small>{{ student.uw_net_id }}</small>
                    </div>
                    <p>
                      <span class="badge rounded-pill border border-muted text-dark me-1">{{
                        student.gender
                      }}</span>
                      <span
                        v-if="student.gender === 'F'"
                        class="badge rounded-pill border border-muted text-dark"
                        >she/her</span
                      >
                      <span v-else class="badge rounded-pill border border-muted text-dark"
                        >he/him</span
                      >
                    </p>
                    <div>
                      <i class="bi bi-trophy-fill text-purple"></i> Sport: Track &amp; Field
                    </div>
                  </div>
                </div>
                <div class="col-6 col-lg-3 px-4 small">
                  <ul class="list-unstyled m-0">
                    <li>
                      Preferred name: {{ student.student_preferred_first_name }}
                      {{ student.student_preferred_middle_name }}
                      {{ student.student_preferred_last_name }}
                    </li>
                    <li>Ethnicity:</li>
                    <li>Citizenship: {{ student.resident_desc }}</li>
                    <li>DOB: 7/23/2001</li>
                  </ul>
                </div>
                <div class="col-6 col-lg-3 ps-4 small">
                  <ul class="list-unstyled m-0">
                    <li>UW Email: {{ student.student_email }}</li>
                    <li>Personal email: {{ student.personal_email }}</li>
                    <li>Local Phone: {{ student.local_phone_number }}</li>
                    <li>Perm Address: {{ studentAddress }}</li>
                    <li>
                      Local Address: 1234
                      <a href="#" class="small" role="button">Edit address (ALL)</a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- notes area -->
        <div class="row">
          <div class="col-xl-9">
            <div class="card border-light-gray shadow-sm rounded-3 mb-4">
              <div class="card-header d-flex justify-content-between bg-white border-0 p-4 pb-0">
                <h2
                  class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
                >
                  Contact
                </h2>
                <p class="text-end"><add-contact></add-contact></p>
              </div>
              <div class="card-body p-4">
                <div class="table-responsive">
                  <table class="table m-0">
                    <thead class="small">
                      <tr>
                        <th>Date</th>
                        <th>Time</th>
                        <th class="text-nowrap">Contact Type</th>
                        <th>Staff</th>
                        <th>Notes</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td scope="row">09/23/2020</td>
                        <td>1:55PM</td>
                        <td>Drop-in</td>
                        <td>Otto Wilson</td>
                        <td>
                          Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam, ducimus
                          mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis doloribus
                          expedita iure fuga obcaecati modi incidunt. Repellendus velit asperiores
                          dolores excepturi?
                          <p class="text-end small"><a href="#">Edit notes</a></p>
                        </td>
                      </tr>
                      <tr>
                        <td scope="row">07/04/2020</td>
                        <td>10:52AM</td>
                        <td>Quick Question</td>
                        <td>Boris Washington</td>
                        <td>
                          Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam, ducimus
                          mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis doloribus
                          expedita iure fuga obcaecati modi incidunt. Repellendus velit asperiores
                          dolores excepturi?
                          <p class="text-end small"><a href="#">Edit notes</a></p>
                        </td>
                      </tr>
                      <tr>
                        <td scope="row">06/29/2020</td>
                        <td>3:15PM</td>
                        <td>Appointment</td>
                        <td>Otto Wilson</td>
                        <td>
                          Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam, ducimus
                          mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis doloribus
                          expedita iure fuga obcaecati modi incidunt. Repellendus velit asperiores
                          dolores excepturi?
                          <p class="text-end small"><a href="#">Edit notes</a></p>
                        </td>
                      </tr>
                      <tr>
                        <td scope="row">5/14/2020</td>
                        <td>2:15PM</td>
                        <td>Telephone</td>
                        <td>Otto Wilson</td>
                        <td>
                          Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam, ducimus
                          mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis doloribus
                          expedita iure fuga obcaecati modi incidunt. Repellendus velit asperiores
                          dolores excepturi?
                          <p class="text-end small"><a href="#">Edit notes</a></p>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          <div class="col-xl-3">
            <!-- adviser -->
            <div class="card border-light-gray shadow-sm rounded-3 mb-4">
              <div class="card-header bg-white border-0 p-4 pb-0">
                <h2
                  class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
                >
                  Adviser
                </h2>
              </div>
              <div class="card-body p-4">
                <ul class="list-unstyled">
                  <li class="fw-bold">John Average</li>
                  <li>he/him</li>
                  <li>Email</li>
                  <li>Phone</li>
                  <li class="border-top mt-2 pt-2">Dept Name: OMAD</li>
                  <li>Campus location: MGH 123</li>
                  <li><a href="#" class="small">Edit adviser (ADMIN)</a></li>
                </ul>

                <div class="border border-danger">
                  <ul class="list-unstyled text-muted">
                    <li><p>This student does not have an assigned adviser.</p></li>
                    <li>
                      <select
                        class="form-select form-select-sm mb-2"
                        aria-label=".form-select-sm example"
                      >
                        <option selected>Select adviser</option>
                        <option value="1">Bob</option>
                        <option value="2">Tim</option>
                        <option value="3">Joe</option>
                      </select>
                    </li>
                    <li class="text-end">
                      <button type="button" class="btn btn-outline-dark-beige btn-sm rounded-pill">
                        Update adviser
                      </button>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <!-- end adviser -->

            <!-- programs -->
            <div class="card border-light-gray shadow-sm rounded-3 mb-4">
              <div class="card-header bg-white border-0 p-4 pb-0">
                <h2
                  class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
                >
                  Programs
                </h2>
              </div>
              <div class="card-body p-4">
                <p>UW Programs (from EDW?)</p>
                <ul>
                  <li>Honor's</li>
                  <li>Dean's List</li>
                  <li>Athletics</li>
                  <li>EOP</li>
                </ul>

                <hr>

                <p>OMAD Programs (if EOP yes)</p>
                <ul>
                  <li>Pre-professional: yes/no</li>
                  <li>IC Eligible: yes/no</li>
                  <li>
                    <template v-if="student.special_program_code"> <b>yes</b>/no </template>
                    <template v-else> CAMP, TRIO SSS, Champions </template>
                  </li>
                </ul>
                <p><a href="#" class="small">Edit Programs (ADMIN)</a></p>
                <div class="border border-danger">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck1" />
                    <label class="form-check-label" for="defaultCheck1">CAMP</label>
                  </div>
                  <div class="form-check">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      value=""
                      id="defaultCheck2"
                    />
                    <label class="form-check-label" for="defaultCheck2">TRIO</label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck3" />
                    <label class="form-check-label" for="defaultCheck3">SSS</label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck4" />
                    <label class="form-check-label" for="defaultCheck4">Champions</label>
                  </div>
                   <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="defaultCheck5" />
                    <label class="form-check-label" for="defaultCheck5">IC Eligible</label>
                  </div>
                  <div class="text-end">
                     <button type="button" class="btn btn-outline-dark-beige btn-sm rounded-pill">
                        Update programs
                      </button>
                  </div>
                </div>
              </div>
            </div>
            <!-- end programs -->
          </div>
        </div>
        <!-- end notes -->

        <div class="row">
          <div class="col-xl-9">
            <!-- schedule -->
            <div class="card border-light-gray shadow-sm rounded-3 mb-4">
              <div class="card-header bg-white p-4 pb-0">
                <h2
                  class="h5 m-0 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige"
                >
                  Schedule
                </h2>
                <ul class="nav nav-tabs border-0 mt-3" id="myTab1" role="tablist">
                  <li class="nav-item" role="presentation">
                    <button
                      class="nav-link active"
                      id="home-tab"
                      data-bs-toggle="tab"
                      data-bs-target="#home"
                      type="button"
                      role="tab"
                      aria-controls="home"
                      aria-selected="true"
                    >
                      Current Quarter
                    </button>
                  </li>
                  <li class="nav-item" role="presentation">
                    <button
                      class="nav-link"
                      id="profile-tab"
                      data-bs-toggle="tab"
                      data-bs-target="#profile"
                      type="button"
                      role="tab"
                      aria-controls="profile"
                      aria-selected="false"
                    >
                      Next Quarter
                    </button>
                  </li>
                  <li class="nav-item" role="presentation">
                    <button
                      class="nav-link"
                      id="contact-tab"
                      data-bs-toggle="tab"
                      data-bs-target="#contact"
                      type="button"
                      role="tab"
                      aria-controls="contact"
                      aria-selected="false"
                    >
                      Quarter After
                    </button>
                  </li>
                </ul>
              </div>
              <div class="card-body p-4">
                <div class="tab-content" id="myTabContent1">
                  <div
                    class="tab-pane fade show active"
                    id="home"
                    role="tabpanel"
                    aria-labelledby="home-tab"
                  >
                    ...
                  </div>
                  <div
                    class="tab-pane fade"
                    id="profile"
                    role="tabpanel"
                    aria-labelledby="profile-tab"
                  >
                    ...
                  </div>
                  <div
                    class="tab-pane fade"
                    id="contact"
                    role="tabpanel"
                    aria-labelledby="contact-tab"
                  >
                    ...
                  </div>
                </div>
              </div>
            </div>
            <!-- end schedule -->

            <!-- history -->
            <div class="card border-light-gray shadow-sm rounded-3 mb-4">
              <div class="card-header bg-white p-4 pb-0">
                <h2
                  class="h5 m-0 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige"
                >
                  History
                </h2>
                <ul class="nav nav-tabs border-0 mt-3" id="myTab" role="tablist">
                  <li class="nav-item" role="presentation">
                    <button
                      class="nav-link active"
                      id="profile-tab"
                      data-bs-toggle="tab"
                      data-bs-target="#visit"
                      type="button"
                      role="tab"
                      aria-controls="visit"
                      aria-selected="false"
                    >
                      Visit (Instructional Center)
                    </button>
                  </li>
                  <li class="nav-item" role="presentation">
                    <button
                      class="nav-link"
                      id="registrations-tab"
                      data-bs-toggle="tab"
                      data-bs-target="#registrations"
                      type="button"
                      role="tab"
                      aria-controls="registrations"
                      aria-selected="false"
                    >
                      Transcript
                    </button>
                  </li>
                  <li class="nav-item" role="presentation">
                    <button
                      class="nav-link"
                      id="major-tab"
                      data-bs-toggle="tab"
                      data-bs-target="#major"
                      type="button"
                      role="tab"
                      aria-controls="major"
                      aria-selected="false"
                    >
                      Major
                    </button>
                  </li>
                </ul>
              </div>
              <div class="card-body p-4">
                <div class="tab-content" id="myTabContent">
                  <div
                    class="tab-pane fade show active"
                    id="visit"
                    role="tabpanel"
                    aria-labelledby="visit-tab"
                  >
                    <div class="table-responsive">
                      <table class="table table-hover table-striped m-0">
                        <thead class="small">
                          <tr>
                            <th>Date</th>
                            <th class="text-nowrap">Location</th>
                            <th>Course</th>
                            <th>Check-in</th>
                            <th>Check-out</th>
                            <th>Duration</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td scope="row">09/23/2020</td>
                            <td>Instructional Center</td>
                            <td>BUS 220</td>
                            <td>10:35am</td>
                            <td>11:42pm</td>
                            <td>1hr 2mins</td>
                          </tr>
                          <tr>
                            <td scope="row">07/04/2020</td>
                            <td>Computer Lab</td>
                            <td>CSE 142</td>
                            <td>9:15am</td>
                            <td>11:2am</td>
                            <td>2 hrs</td>
                          </tr>
                          <tr>
                            <td scope="row">06/29/2020</td>
                            <td>Instruction Center</td>
                            <td>BUS 220</td>
                            <td>4:31pm</td>
                            <td>4:45pm</td>
                            <td>15 mins</td>
                          </tr>
                          <tr>
                            <td scope="row">5/14/2020</td>
                            <td>Instructional Center</td>
                            <td>BUS 220</td>
                            <td>2:34pm</td>
                            <td>6:35pm</td>
                            <td>4 hrs</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                  <div
                    class="tab-pane fade"
                    id="registrations"
                    role="tabpanel"
                    aria-labelledby="registrations-tab"
                  >
                    <div class="table-responsive">
                      <table class="table table-hover table-striped m-0">
                        <thead class="small">
                          <tr>
                            <th>Course</th>
                            <th>Credits</th>
                            <th>Grade</th>
                            <th>Year</th>
                            <th>Quarter</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>BIOL 350</td>
                            <td>3</td>
                            <td>3.8</td>
                            <td>2021</td>
                            <td>Spring</td>
                          </tr>
                          <tr>
                            <td>CHEM 238</td>
                            <td>4</td>
                            <td>4.0</td>
                            <td>2021</td>
                            <td>Autumn</td>
                          </tr>
                          <tr>
                            <td>MATH 210</td>
                            <td>5.0</td>
                            <td>W4</td>
                            <td>2021</td>
                            <td>Autumn</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <div class="tab-pane fade" id="major" role="tabpanel" aria-labelledby="major-tab">
                    <div class="table-responsive">
                      <h3
                        class="h6 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige"
                      >
                        Accepted Major
                      </h3>
                      <table class="table table-hover table-striped m-0 mb-3">
                        <thead class="small">
                          <tr>
                            <th>Date</th>
                            <th>Major</th>
                            <th>Status</th>
                            <th class="text-nowrap">Source</th>
                            <th>Action</th>
                            <th>Notes</th>
                            <th>User</th>
                          </tr>
                        </thead>
                        <tbody class="mb-3">
                          <tr>
                            <td scope="row">10/01/2021</td>
                            <td>Psychology</td>
                            <td>Accepted</td>
                            <td>SWS</td>
                            <td></td>
                            <td></td>
                            <td></td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <div class="table-responsive">
                      <h3
                        class="h6 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige"
                      >
                        Intended Major
                      </h3>
                      <table class="table table-hover table-striped m-0 mb-3">
                        <thead class="small">
                          <tr>
                            <th>Date</th>
                            <th>Major</th>
                            <th>Status</th>
                            <th class="text-nowrap">Source</th>
                            <th>Action</th>
                            <th>Notes</th>
                            <th>User</th>
                          </tr>
                        </thead>
                        <tbody class="mb-3">
                          <tr>
                            <td scope="row">9/23/2020</td>
                            <td>Computer Engineering</td>
                            <td>Intended #1</td>
                            <td>DawgPath</td>
                            <td>Remove</td>
                            <td>No longer interested</td>
                            <td>Student</td>
                          </tr>
                          <tr>
                            <td scope="row">7/04/2020</td>
                            <td>Human Centered Design &amp; Engineering</td>
                            <td>Intended #2</td>
                            <td>Compass</td>
                            <td>Add</td>
                            <td>Wants to be a UX Designer</td>
                            <td>Pedro Sanchez</td>
                          </tr>
                          <tr>
                            <td scope="row">6/29/2020</td>
                            <td>Accounting</td>
                            <td>Intended #3</td>
                            <td>Compass</td>
                            <td>Remove</td>
                            <td>Does not like numbers</td>
                            <td>Pedro Sanchez</td>
                          </tr>
                          <tr>
                            <td scope="row">5/23/2020</td>
                            <td>Economics</td>
                            <td>Intended #3</td>
                            <td>DawgPath</td>
                            <td>Remove</td>
                            <td>n/a</td>
                            <td>Student</td>
                          </tr>
                        </tbody>
                      </table>
                      <h3
                        class="h6 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige"
                      >
                        Intended Major upon Admission
                      </h3>
                      <table class="table table-hover table-striped m-0">
                        <thead class="small">
                          <tr>
                            <th>Date</th>
                            <th>Major</th>
                            <th>Status</th>
                            <th class="text-nowrap">Source</th>
                            <th>Action</th>
                            <th>Notes</th>
                            <th>User</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td scope="row">5/14/2020</td>
                            <td>Informatics</td>
                            <td>Intended #3</td>
                            <td>Admissions</td>
                            <td></td>
                            <td></td>
                            <td></td>
                          </tr>
                          <tr>
                            <td scope="row">5/14/2020</td>
                            <td>Computer Science</td>
                            <td>Intended #2</td>
                            <td>Admissions</td>
                            <td></td>
                            <td></td>
                            <td></td>
                          </tr>
                          <tr>
                            <td scope="row">5/14/2020</td>
                            <td>Anthropolgy</td>
                            <td>Intended #1</td>
                            <td>Admissions</td>
                            <td></td>
                            <td></td>
                            <td></td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
                <!-- end card-body -->
              </div>
            </div>
            <!-- end history -->
          </div>
          <div class="col-xl-3">
            <!-- MARK: card component styling -->
            <div class="card border-light-gray shadow-sm rounded-3 mb-4">
              <div class="card-header bg-white border-0 p-4 pb-0">
                <h2
                  class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
                >
                  Retention
                </h2>
              </div>
              <div class="card-body p-4">
                <ul>
                  <li>
                    Priority: <span class="fw-bold">{{ student.retention.priority }}</span>
                  </li>
                  <li>Sign-ins: {{ student.retention.sign_in }}</li>
                  <li>Activity: {{ student.retention.activity }}</li>
                  <li>Assignments: {{ student.retention.assignment }}</li>
                  <li>Grades: {{ student.retention.grade }}</li>
                </ul>
              </div>
            </div>

            <div class="card border-light-gray shadow-sm rounded-3 mb-4">
              <div class="card-header bg-white border-0 p-4 pb-0">
                <h2
                  class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
                >
                  Academics
                </h2>
              </div>
              <div class="card-body p-4">
                <ul>
                  <li>
                    Registered:
                    <template v-if="student.registered_in_quarter"> <b>yes</b>/no </template>
                    <template v-else>
                      yes/
                      <b>no</b>
                    </template>
                  </li>
                  <li>Enrollment Status: {{ student.enrollment_desc }}</li>
                  <li>Class standing: {{ student.class_desc }}</li>
                  <li>Total Credits: {{ student.total_credits }}</li>
                  <li>Total UW Credits: 170.00</li>
                  <li>Transfer student: <b>yes</b>/no</li>
                  <li>GPA: {{ student.gpa }}</li>
                </ul>
              </div>
            </div>

            <div class="card border-light-gray shadow-sm rounded-3 mb-4">
              <div class="card-header bg-white border-0 p-4 pb-0">
                <h2
                  class="h5 m-0 text-uppercase axdd-font-encode-sans fw-bold text-uppercase text-dark-beige"
                >
                  Major
                </h2>
              </div>
              <div class="card-body p-4">
                <ul>
                  <li>
                    Accepted:
                    <span v-for="(major, index) in student.major" :key="index">
                      {{ major.major_full_name }}
                      <span v-if="index + 1 < student.major.length">,</span>
                    </span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- history -->
        <div class="row">
          <div class="col"></div>
        </div>
        <!-- end history -->
      </div>
      <div v-else>No student</div>
    </template>
  </layout>
</template>

<script>
import { Card } from 'axdd-components';
import Layout from '../layout.vue';
import dataMixin from '../mixins/data_mixin.js';
import AddContact from '../components/add-contact.vue';

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    'axdd-card': Card,
    'add-contact': AddContact,
  },
  created: function () {
    this.loadstudent(this.$route.params.id);
  },
  data() {
    return {
      student: {},
    };
  },
  computed: {
    studentAddress: function () {
      let addr = '';
      if (this.student.perm_addr_line1) addr += this.student.perm_addr_line1 + ' ';
      if (this.student.perm_addr_line2) addr += this.student.perm_addr_line2 + ' ';
      if (this.student.perm_addr_city) addr += this.student.perm_addr_city;
      if (this.student.perm_addr_state) addr += ', ' + this.student.perm_addr_state;
      if (this.student.perm_addr_line1) addr += ' ' + this.student.perm_addr_postal_code;
      if (addr) return addr;
      else return 'N/A';
    },
    priorityRing: function () {
      // mocked display
      if (this.student.retention.priority === '-3.4') {
        return 'border-danger';
      } else if (this.student.retention.priority === '2.2') {
        return 'border-warning';
      } else {
        return '';
      }
    },
  },
  methods: {
    loadstudent: function (studentNumber) {
      let _this = this;
      this.getStudentDetail(studentNumber).then((response) => {
        if (response.data) {
          _this.student = response.data[0];
        }
      });
    },
  },
};
</script>

<style lang="scss">
.table {
  tr:last-of-type {
    border-color: transparent !important;
  }
}
</style>
