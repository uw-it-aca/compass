// about.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      <div v-if="$route.params.id" class="mb-3">
        <div class="row">
          <div class="col-lg-6 d-flex">
            <div style="width:130px;">
              <img src="/static/img/napoleon-dynamite.jpeg" class="img-fluid rounded-circle border border-danger border-5" alt="">
              <div class="text-center text-muted mb-4">priority: <span class="text-danger">TOP</span></div>
            </div>
            <div class="flex-fill ps-3 mb-4">
              <h1 class="h3 text-uppercase">{{student.student_name}}</h1>
              <div class="h5">{{ $route.params.id }}</div>
              <p>{{student.uw_net_id}}, {{student.gender}}, Pronouns</p>
              <div><i class="bi bi-trophy-fill text-purple"></i> Student Athlete</div>
            </div>
          </div>
          <div class="col-6 col-lg-3 border-start">
            <ul class="list-unstyled m-0">
              <li>Preferred name: {{student.student_preferred_first_name}} {{student.student_preferred_middle_name}} {{student.student_preferred_last_name}}</li>
              <li>Ethnicity:</li>
              <li>Citizenship: {{student.resident_desc}}</li>
            </ul>
          </div>
          <div class="col-6 col-lg-3 border-start">
            <ul class="list-unstyled m-0">
              <li>UW Email: {{student.student_email}}</li>
              <li>Personal email: {{student.personal_email}}</li>
              <li>Phone: {{student.local_phone_number}}</li>
              <li>Address: {{studentAddress}}</li>
            </ul>
          </div>
        </div>
      </div>
      <h1 v-else>Student</h1>
    </template>

    <template #content>
      <div v-if="$route.params.id">
        <div class="row mb-3">
          <div class="col text-end">
            <a class="btn btn-outline-primary border m-1 shadow-sm" href="#" role="button"  data-bs-toggle="modal" data-bs-target="#exampleModal" style="font-size: 20px;">
              <i class="bi bi-chat-square-text"></i>
            </a>
          </div>
        </div>

        <!-- academics area -->
        <div class="row">
          <div class="col-md-4">
            <div class="card shadow-sm mb-3">
              <div class="card-body">
                <h3 class="card-title h6 text-uppercase text-muted fw-bold">Academics</h3>
                <ul>
                  <li>Registered:
                    <template v-if="student.registered_in_quarter">
                      <b>yes</b>/no
                    </template>
                    <template v-else>
                      yes/<b>no</b>
                    </template>
                  </li>
                  <li>Enrollment Status: {{student.enrollment_desc}}</li>
                  <li>Class standing: {{student.class_desc}}</li>
                  <li>Total Credits: {{student.total_credits}}</li>
                  <li>GPA: {{student.gpa}}</li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card shadow-sm mb-3">
              <div class="card-body">
                <h3 class="card-title h6 text-uppercase text-muted fw-bold">OMAD Programs</h3>
                <ul>
                  <li>EOP: yes/no</li>
                  <li>Pre-professional: yes/no</li>
                  <li>IC Eligible: yes/no</li>
                  <li>Special program:
                    <template v-if="student.special_program_code">
                      <b>yes</b>/no
                    </template>
                    <template v-else>
                      yes/<b>no</b>
                    </template>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card shadow-sm mb-3">
              <div class="card-body">
                <h3 class="card-title h6 text-uppercase text-muted fw-bold">Adviser</h3>

                <div class="d-flex">
                  <div style="width: 65px;">
                    <img src="/static/img/pedro-sanchez.jpeg" class="img-fluid rounded-circle border border-3" alt="">
                  </div>
                  <div class="flex-fill ps-3">
                    <ul class="list-unstyled">
                      <li class="fw-bold">Pedro Sanchez</li>
                      <li>Email</li>
                      <li>Phone</li>
                      <li class="border-top mt-2 pt-2">Department Name</li>
                      <li>Campus location</li>
                    </ul>
                  </div>
                </div>
                <div class="text-end"><a href="#">View caseload</a></div>
              </div>
              <div class="card-footer">
                <div class="input-group">
                  <select class="form-select form-select-sm" id="inputGroupSelect04" aria-label="Example select with button addon">
                    <option selected>Pedro Sanchez</option>
                    <option value="1">Bill Thompson</option>
                    <option value="2">Doris Washington</option>
                  </select>
                  <button class="btn btn-sm btn-outline-primary" type="button">update</button>
                </div>
                <div class="small text-danger">Admins can re-assign advisers</div>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card shadow-sm mb-3">
              <div class="card-body">
                <h3 class="card-title h6 text-uppercase text-muted fw-bold">Major</h3>
                <ul>
                  <li>Desired major: 
                    <span v-for="(major, index) in student.intended_major" :key="index">{{major.major_full_name}}<span v-if="index+1 < student.intended_major.length">, </span></span>
                    <a href="#" class="btn btn-sm btn-outline-primary py-0" role="button">change</a>
                  </li>
                  <li>Accepted major:
                    <span v-for="(major, index) in student.major" :key="index">{{major.major_full_name}}<span v-if="index+1 < student.major.length">, </span></span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card shadow-sm mb-3">
              <div class="card-body">
                <h3 class="card-title h6 text-uppercase text-muted fw-bold">Schedule</h3>
                <ul>
                  <li>curent quarter</li>
                  <li>class schedule</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <!-- end academics -->
        <!-- notes area -->
        <div class="row">
          <div class="col">
            <ul class="nav nav-tabs" id="myTab" role="tablist">
              <li class="nav-item" role="presentation">
                <button class="nav-link active" id="home-tab" data-bs-toggle="tab" data-bs-target="#home" type="button" role="tab" aria-controls="home" aria-selected="true">Contact History</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="profile-tab" data-bs-toggle="tab" data-bs-target="#profile" type="button" role="tab" aria-controls="profile" aria-selected="false">IC Visits</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="contact-tab" data-bs-toggle="tab" data-bs-target="#contact" type="button" role="tab" aria-controls="contact" aria-selected="false">Additional Student Info</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="major-tab" data-bs-toggle="tab" data-bs-target="#major" type="button" role="tab" aria-controls="majors" aria-selected="false">Intended Major</button>
              </li>
            </ul>
            <div class="tab-content bg-white border-start border-end border-bottom mb-5 p-3 rounded-bottom shadow-sm" id="myTabContent">
              <div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
                <div class="table-responsive">
                  <table class="table table-hover table-striped">
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
                        <th scope="row">09/23/2020</th>
                        <td>1:55PM</td>
                        <td>Drop-in</td>
                        <td>Otto Wilson</td>
                        <td>
                          Lorem ipsum dolor sit amet consectetur adipisicing elit.
                          Totam, ducimus mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis
                          doloribus expedita iure fuga obcaecati modi incidunt. Repellendus velit
                          asperiores dolores excepturi?
                        </td>
                      </tr>
                      <tr>
                        <th scope="row">07/04/2020</th>
                        <td>10:52AM</td>
                        <td>Quick Question</td>
                        <td>Boris Washington</td>
                        <td>
                          Lorem ipsum dolor sit amet consectetur adipisicing elit.
                          Totam, ducimus mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis
                          doloribus expedita iure fuga obcaecati modi incidunt. Repellendus velit
                          asperiores dolores excepturi?
                        </td>
                      </tr>
                      <tr>
                        <th scope="row">06/29/2020</th>
                        <td>3:15PM</td>
                        <td>Appointment</td>
                        <td>Otto Wilson</td>
                        <td>
                          Lorem ipsum dolor sit amet consectetur adipisicing elit.
                          Totam, ducimus mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis
                          doloribus expedita iure fuga obcaecati modi incidunt. Repellendus velit
                          asperiores dolores excepturi?
                        </td>
                      </tr>
                      <tr>
                        <th scope="row">5/14/2020</th>
                        <td>2:15PM</td>
                        <td>Telephone</td>
                        <td>Otto Wilson</td>
                        <td>
                          Lorem ipsum dolor sit amet consectetur adipisicing elit.
                          Totam, ducimus mollitia! Maiores suscipit tempore sunt, ipsa beatae omnis
                          doloribus expedita iure fuga obcaecati modi incidunt. Repellendus velit
                          asperiores dolores excepturi?
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">profile</div>
              <div class="tab-pane fade" id="contact" role="tabpanel" aria-labelledby="contact-tab">contact</div>
              <div class="tab-pane fade" id="major" role="tabpanel" aria-labelledby="major-tab">major</div>
            </div>
          </div>
        </div>
        <!-- end notes -->
      </div>
      <div v-else>No student</div>

      <!-- visit modal -->
      <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLabel">Record a contact</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="row mb-3">
                <div class="col">
                  <label for="date" class="form-label">Date:</label>
                  <input type="date" id="date" class="form-control">
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
                      <label for="appt-time" class="form-label">Check in time: </label>
                      <input id="appt-time" type="time" name="appt-time" value="13:30" class="form-control">
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
                <div style="column-count: 3;">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="flexCheck1">
                    <label class="form-check-label" for="flexCheck1">
                      Add/Drop Class
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="flexCheck2">
                    <label class="form-check-label" for="flexCheck2">
                      Join/Affiliate
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="flexCheck3">
                    <label class="form-check-label" for="flexCheck3">
                      Academic Difficulties
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="flexCheck4">
                    <label class="form-check-label" for="flexCheck4">
                      Hardship Withdrawl
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="flexCheck5">
                    <label class="form-check-label" for="flexCheck5">
                      Internships
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="flexCheck6">
                    <label class="form-check-label" for="flexCheck6">
                      Research Opportunities
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="flexCheck7">
                    <label class="form-check-label" for="flexCheck7">
                      Graduate Professional School
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="flexCheck8">
                    <label class="form-check-label" for="flexCheck8">
                      Testing/Assessment
                    </label>
                  </div>
                </div>
              </div>
              <div class="mb-3">
                <label for="exampleFormControlTextarea1" class="form-label">Notes</label>
                <textarea class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
              </div>

              <div class="mb-3">
                <label for="exampleFormControlTextarea2" class="form-label">Actions and Recommmendations</label>
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
    layout: Layout,
    'axdd-card': Card,
  },
  created: function() {
    this.loadstudent(this.$route.params.id);
  },
  data() {
    return {
      student: {},
      pageTitle: '',
    };
  },
  computed: {
    studentAddress: function () {
      let addr = "";
      if (this.student.perm_addr_line1)
        addr += (this.student.perm_addr_line1 + " ");
      if (this.student.perm_addr_line2)
        addr += (this.student.perm_addr_line2 + " ");
      if (this.student.perm_addr_city )
        addr += this.student.perm_addr_city;
      if (this.student.perm_addr_state)
        addr += (", " + this.student.perm_addr_state);
      if (this.student.perm_addr_line1)
        addr += (" " + this.student.perm_addr_postal_code);
      if (addr)
        return addr;
      else
        return "N/A";
    },
  },
  methods: {
    loadstudent: function(studentNumber) {
      let _this = this;
      this.getStudentDetail(studentNumber).then(response => {
        if (response.data) {
          _this.student = response.data[0];
          _this.student.pageTitle = (
            _this.student.student_name + " (" + _this.student.student_number + ")"
          );
        }
      });
    }
  },
};
</script>

<style lang="scss"></style>
