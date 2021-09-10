// about.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      <div v-if="$route.params.id" class="border-bottom mb-3">
        <div class="d-flex">
          <div class="flex-fill">
            <h1 class="h3 text-uppercase">Dynamite, Napoleon</h1>
            <h2 class="h3">{{ $route.params.id }}</h2>
          </div>
          <div class="flex-fill text-end text-nowrap">
            <a class="btn btn-outline-light border text-muted me-2 shadow-sm" href="#" role="button" style="font-size: 20px;">
              <i class="bi bi-telephone"></i>
            </a>
            <a class="btn btn-outline-primary border shadow-sm" href="#" role="button"  data-bs-toggle="modal" data-bs-target="#exampleModal" style="font-size: 20px;">
              <i class="bi bi-chat-square-text"></i>
            </a>
          </div>
        </div>
      </div>
      <h1 v-else>Student</h1>
    </template>

    <template #content>
      <div v-if="$route.params.id">
        <div class="row">
          <div class="col-sm-8">
            <div class="card shadow-sm mb-3">
              <div class="row">
                <div class="col-4">
                  <img src="/static/img/napoleon-dynamite.jpeg" class="img-fluid rounded-start" alt="">
                </div>
                <div class="col-8">
                  <div class="card-body px-0">
                    <h3 class="card-title">Profile</h3>
                    <ul>
                      <li>StudentID Photo</li>
                      <li>Preferred Name</li>
                      <li>Pronouns</li>
                      <li>UW NetId</li>
                      <li>DOB</li>
                      <li>Ethnicity</li>
                      <li>Gender</li>
                      <li>Citizenship</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-sm-4">
            <div class="card shadow-sm mb-3">
              <div class="card-body">
                <h3 class="card-title">Contact</h3>
                <ul>
                  <li>UW Email</li>
                  <li>Personal email</li>
                  <li>Phone</li>
                  <li>Address</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <!-- academics area -->
        <div class="row">
          <div class="col-sm-4">
            <div class="card shadow-sm mb-3">
              <div class="card-body">
                <h3 class="card-title">Standing</h3>
                <ul>
                  <li>Registered yes/no</li>
                  <li>Enrollment Status yes/no</li>
                  <li>Class standing (freshman, sophmore, etc.)</li>
                  <li>Total Credits</li>
                  <li>GPA</li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-sm-4">
            <div class="card shadow-sm mb-3">
              <div class="card-body">
                <h3 class="card-title">OMAD Specific?</h3>
                <ul>
                  <li>EOP - 13 yes/no</li>
                  <li>Pre-professional yes/no</li>
                  <li>IC Eligible yes/no</li>
                  <li>Special program yes/no</li>
                </ul>
              </div>
            </div>
          </div>
          <div class="col-sm-4">
            <div class="card shadow-sm mb-3">
              <div class="card-body">
                <h3 class="card-title">Academics</h3>
                <ul>
                  <li>Adviser Name: 
                    <div class="input-group">
                      <select class="form-select form-select-sm" id="inputGroupSelect04" aria-label="Example select with button addon">
                        <option selected>Pedro Sanchez</option>
                        <option value="1">Bill Thompson</option>
                        <option value="2">Doris Washington</option>
                      </select>
                      <button class="btn btn-sm btn-outline-primary" type="button" data-bs-toggle="modal" data-bs-target="#adviserModal">view</button>
                    </div>
                  </li>
                  <li>Active? yes/no</li>
                  <li>Intended Major/Degree (as of quarter? timestamp) <a href="#" class="btn btn-sm btn-outline-primary py-0" role="button">change</a></li>
                  <li>Accepted Major</li>
                  <li>Current Schedule (current quarter)</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <!-- end academics -->
        <!-- notes area -->
        <div class="row">
          <div class="col">
            <ul class="nav nav-tabs">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#">Visit History</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">IC Summary</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Additional Student Info</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Intended Major (change history)</a>
              </li>
            </ul>
            <div class="bg-white border-start border-end border-bottom mb-5 p-3 rounded-bottom shadow-sm">
            <table class="table table-hover table-striped">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th class="text-nowrap">Contact Type</th>
                  <th class="text-nowrap">Event Type</th>
                  <th>Staff</th>
                  <th>Notes</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">09/23/2020</th>
                  <td>1:55PM</td>
                  <td>Drop-in</td>
                  <td></td>
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
                  <td></td>
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
                  <td></td>
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
        </div>
        <!-- end notes -->
      </div>
      <div v-else>No student</div>

      <!-- visit modal -->
      <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLabel">In-person visit</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="row mb-3"> 
                <div class="col">
                  <label for="date">Date:</label>
                  <input type="date" id="date" class="form-control">
                </div>
                <div class="col">
                  Contact type:
                  <select class="form-select" aria-label="Default select example">
                    <option selected>Quick Question</option>
                    <option value="1">Appointment</option>
                    <option value="2">Drop-in</option>
                  </select>
                </div>
                <div class="col">
                  Visit duration (min):
                  <select class="form-select" aria-label="Default select example">
                    <option selected>15</option>
                    <option value="1">30</option>
                    <option value="2">60</option>
                    <option value="3">90</option>
                  </select>
                </div>
              </div>
              <div class="mb-3">
                Topics Covered
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
              <button type="button" class="btn btn-primary">Save visit</button>
            </div>
          </div>
        </div>
      </div>
      <!-- end visit modal -->

      <!-- adviser modal -->
      <div class="modal fade" id="adviserModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Pedro Sanchez</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div style="width: 150px;">
                <img src="/static/img/pedro-sanchez.jpeg" class="img-fluid img-thumbnail" alt="">
              </div>
              <ul>
                <li>Department Name</li>
                <li>Campus location</li>
                <li>Phone</li>
                <li>Email</li>
              </ul>
              <p><a href="#">View caseload</a></p>
            </div>
          </div>
        </div>
      </div>
      <!-- end adviser modal -->
    </template>
  </layout>
</template>

<script>
import { Card } from 'axdd-components';
import Layout from '../layout.vue';
import HelloWorld from '../components/hello-world.vue';

export default {
  components: {
    layout: Layout,
    'hello-world': HelloWorld,
    'axdd-card': Card,
  },
  data() {
    return {
      pageTitle: 'Average, John #12345678',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
