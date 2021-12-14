// about.vue

<template>
  <layout v-if="student.student_name !== undefined" :page-title="student.student_name">
    <template #title>
      <h1 v-if="$route.params.id" class="visually-hidden">{{ student.student_name }}</h1>
      <h1 v-else>Student</h1>
    </template>
    <template #content>
      <div v-if="$route.params.id">
        <div class="row mb-3">
          <div class="col-lg-6 d-flex">
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
                <span class="fw-bold">LEVEL {{ student.retention.priority }}</span>
              </div>
            </div>
            <div class="flex-fill ps-3 mb-4">
              <div class="h3 text-uppercase">
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
                <span v-else class="badge rounded-pill border border-muted text-dark">he/him</span>
              </p>
              <div><i class="bi bi-trophy-fill text-purple"></i> Student Athlete</div>
            </div>
          </div>
          <div class="col-6 col-lg-3 border-start">
            <ul class="list-unstyled m-0">
              <li>
                Preferred name: {{ student.student_preferred_first_name }}
                {{ student.student_preferred_middle_name }}
                {{ student.student_preferred_last_name }}
              </li>
              <li>Ethnicity:</li>
              <li>Citizenship: {{ student.resident_desc }}</li>
            </ul>
          </div>
          <div class="col-6 col-lg-3 border-start">
            <ul class="list-unstyled m-0">
              <li>UW Email: {{ student.student_email }}</li>
              <li>Personal email: {{ student.personal_email }}</li>
              <li>Phone: {{ student.local_phone_number }}</li>
              <li>Address: {{ studentAddress }}</li>
            </ul>
          </div>
        </div>
        <div class="row mb-3">
          <div class="col text-end">
            <a
              class="btn btn-outline-primary border m-1 shadow-sm"
              href="#"
              role="button"
              data-bs-toggle="modal"
              data-bs-target="#exampleModal"
              style="font-size: 20px"
            >
              <i class="bi bi-chat-square-text"></i>
            </a>
          </div>
        </div>

        <!-- academics area -->
        <div class="row">
          <div class="col-md-4">
            <div class="card shadow-sm mb-3">
              <h3
                class="card-header h6 text-uppercase text-muted fw-bold"
                style="line-height: 30px"
              >
                Retention
              </h3>
              <div class="card-body">
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
            <div class="card shadow-sm mb-3">
              <h3
                class="card-header h6 text-uppercase text-muted fw-bold"
                style="line-height: 30px"
              >
                Academics
              </h3>
              <div class="card-body">
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
                  <li>GPA: {{ student.gpa }}</li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card shadow-sm mb-3">
              <h3
                class="card-header h6 text-uppercase text-muted fw-bold"
                style="line-height: 30px"
              >
                Programs
              </h3>
              <div class="card-body">
                <ul>
                  <li>EOP: yes/no</li>
                  <li>Pre-professional: yes/no</li>
                  <li>IC Eligible: yes/no</li>
                  <li>
                    Special program:
                    <template v-if="student.special_program_code"> <b>yes</b>/no </template>
                    <template v-else>
                      yes/
                      <b>no</b>
                    </template>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card shadow-sm mb-3">
              <h3
                class="card-header h6 text-uppercase text-muted fw-bold"
                style="line-height: 30px"
              >
                Adviser
              </h3>
              <div class="card-body">
                <div class="d-flex">
                  <div style="width: 65px">
                    <img
                      :src="
                        'https://randomuser.me/api/portraits/men/29.jpg'
                      "
                      class="img-fluid rounded-circle border border-3"
                    />
                  </div>
                  <div class="flex-fill ps-3">
                    <ul class="list-unstyled">
                      <li class="fw-bold">John Average</li>
                      <li>Email</li>
                      <li>Phone</li>
                      <li class="border-top mt-2 pt-2">Department Name</li>
                      <li>Campus location</li>
                    </ul>
                  </div>
                </div>
                <div class="text-end">
                  <a href="/adviser/javerage">View caseload</a>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card shadow-sm mb-3">
              <h3
                class="card-header h6 text-uppercase text-muted fw-bold"
                style="line-height: 30px"
              >
                Majors
              </h3>
              <div class="card-body">
                <ul class="list-unstyled">
                  <li>
                    Intended #1: Anthropology
                    <span v-for="(major, index) in student.intended_major" :key="index">
                      {{ major.major_full_name }}
                      <span v-if="index + 1 < student.intended_major.length">,</span>
                    </span>
                    <a href="#" class="btn btn-sm btn-outline-primary py-0" role="button">update</a>
                  </li>
                  <li>
                    Intended #2: Computer Science
                    <span v-for="(major, index) in student.intended_major" :key="index">
                      {{ major.major_full_name }}
                      <span v-if="index + 1 < student.intended_major.length">,</span>
                    </span>
                    <a href="#" class="btn btn-sm btn-outline-primary py-0" role="button">update</a>
                  </li>
                  <li>
                    Intended #3: Informatics
                    <span v-for="(major, index) in student.intended_major" :key="index">
                      {{ major.major_full_name }}
                      <span v-if="index + 1 < student.intended_major.length">,</span>
                    </span>
                    <a href="#" class="btn btn-sm btn-outline-primary py-0" role="button">update</a>
                  </li>
                  <hr />
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
          <div class="col-md-4">
            <div class="card shadow-sm mb-3">
              <h3
                class="card-header h6 text-uppercase text-muted fw-bold"
                style="line-height: 30px"
              >
                Schedule
              </h3>
              <div class="card-body">
                <ul>
                  <li>curent quarter</li>
                  <li>class schedule</li>
                </ul>
              </div>
              <div class="card-footer">
                <small class="text-muted">Last updated 3 mins ago</small>
              </div>
            </div>
          </div>
        </div>
        <!-- end academics -->
        <!-- notes area -->
        <div class="row">
          <div class="col">
            <div class="card shadow-sm mb-3">
              <div class="card-header">
                <div class="position-relative">
                  <h3
                    class="
                      card-title
                      h6
                      text-uppercase text-muted
                      fw-bold
                      m-0
                      position-absolute
                      top-50
                      translate-middle-y
                    "
                  >
                    History
                  </h3>
                  <ul
                    class="nav nav-tabs justify-content-end card-header-tabs"
                    id="myTab"
                    role="tablist"
                  >
                    <li class="nav-item" role="presentation">
                      <button
                        class="nav-link active"
                        id="home-tab"
                        data-bs-toggle="tab"
                        data-bs-target="#contact"
                        type="button"
                        role="tab"
                        aria-controls="contact"
                        aria-selected="true"
                      >
                        Contact
                      </button>
                    </li>
                    <li class="nav-item" role="presentation">
                      <button
                        class="nav-link"
                        id="profile-tab"
                        data-bs-toggle="tab"
                        data-bs-target="#visit"
                        type="button"
                        role="tab"
                        aria-controls="visit"
                        aria-selected="false"
                      >
                        Visit
                      </button>
                    </li>
                    <li class="nav-item" role="presentation">
                      <button
                        class="nav-link"
                        id="transcript-tab"
                        data-bs-toggle="tab"
                        data-bs-target="#transcript"
                        type="button"
                        role="tab"
                        aria-controls="transcript"
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
              </div>
              <div class="card-body">
                <div class="tab-content" id="myTabContent">
                  <div
                    class="tab-pane fade show active"
                    id="contact"
                    role="tabpanel"
                    aria-labelledby="contact-tab"
                  >
                    <div class="table-responsive">
                      <table class="table table-hover table-striped m-0">
                        <thead>
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
                              Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam,
                              ducimus mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis
                              doloribus expedita iure fuga obcaecati modi incidunt. Repellendus
                              velit asperiores dolores excepturi?
                            </td>
                          </tr>
                          <tr>
                            <td scope="row">07/04/2020</td>
                            <td>10:52AM</td>
                            <td>Quick Question</td>
                            <td>Boris Washington</td>
                            <td>
                              Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam,
                              ducimus mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis
                              doloribus expedita iure fuga obcaecati modi incidunt. Repellendus
                              velit asperiores dolores excepturi?
                            </td>
                          </tr>
                          <tr>
                            <td scope="row">06/29/2020</td>
                            <td>3:15PM</td>
                            <td>Appointment</td>
                            <td>Otto Wilson</td>
                            <td>
                              Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam,
                              ducimus mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis
                              doloribus expedita iure fuga obcaecati modi incidunt. Repellendus
                              velit asperiores dolores excepturi?
                            </td>
                          </tr>
                          <tr>
                            <td scope="row">5/14/2020</td>
                            <td>2:15PM</td>
                            <td>Telephone</td>
                            <td>Otto Wilson</td>
                            <td>
                              Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam,
                              ducimus mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis
                              doloribus expedita iure fuga obcaecati modi incidunt. Repellendus
                              velit asperiores dolores excepturi?
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                  <div class="tab-pane fade" id="visit" role="tabpanel" aria-labelledby="visit-tab">
                    <div class="table-responsive">
                      <table class="table table-hover table-striped m-0">
                        <thead>
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
                    id="transcript"
                    role="tabpanel"
                    aria-labelledby="transcript-tab"
                  >
                    <div class="table-responsive">
                      <table class="table table-hover table-striped m-0">
                        <thead>
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
                      <table class="table table-hover table-striped m-0">
                        <thead>
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
                            <td scope="row">10/01/2021</td>
                            <td>Psychology</td>
                            <td>Accepted</td>
                            <td>SWS</td>
                            <td></td>
                            <td></td>
                            <td></td>
                          </tr>
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
          </div>
        </div>
        <!-- end notes -->
      </div>
      <div v-else>No student</div>

      <!-- visit modal -->
      <div
        class="modal fade"
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
  </layout>
</template>

<script>
import { Card } from 'axdd-components';
import Layout from '../layout.vue';
import dataMixin from '../mixins/data_mixin.js';

export default {
  mixins: [dataMixin],
  components: {
    'layout': Layout,
    'axdd-card': Card,
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
    }
  },
  methods: {
    loadstudent: function (studentNumber) {
      let _this = this;
      this.getStudentDetail(studentNumber).then((response) => {
        if (response.data) {
          _this.student = response.data[0];
        }
      });
    }
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
