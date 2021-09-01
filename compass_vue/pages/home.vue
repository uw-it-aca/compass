// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #title>
      <h1 class="visually-hidden">{{ pageTitle }}</h1>
    </template>

    <template #content>
      <div class="row justify-content-between mt-5 mb-2">
        <div class="col-sm-4">
          <div class="small">
            <div class="d-inline me-3 text-nowrap">Find student by:</div>
            <div class="d-inline text-nowrap">
              <div class="form-check form-check-inline">
                <input class="form-check-input" checked type="radio" name="inlineRadioOptions" id="inlineRadio1" value="option1">
                <label class="form-check-label" for="inlineRadio1">Number</label>
              </div>
              <div class="form-check form-check-inline">
                <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="option2">
                <label class="form-check-label" for="inlineRadio2">Name</label>
              </div>
              <div class="form-check form-check-inline">
                <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio3" value="option3">
                <label class="form-check-label" for="inlineRadio3">Email</label>
              </div>
            </div>
          </div>
          <div class="input-group input-group-sm mb-3">
            <input type="text" class="form-control" placeholder="Recipient's username" aria-label="Recipient's username" aria-describedby="button-addon2">
            <button class="btn btn-outline-secondary" type="button" id="button-addon2">GO</button>
          </div>
        </div>
        <div class="col-sm-4">
          <div class="small">Select advisor caseload:</div>
          <select class="form-select form-select-sm" aria-label="Default select example">
            <option selected>All advisers</option>
            <option value="1">Jon Average</option>
            <option value="2">April Foolery</option>
            <option value="3">Bob Samsonite</option>
          </select>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <div class="table-responsive">
            <table class="table table-striped table-hover border">
              <thead>
                <tr>
                  <th scope="col">Name</th>
                  <th scope="col">Student Number</th>
                  <th scope="col">UW NetID</th>
                  <th scope="col">Class</th>
                  <th scope="col">Major</th>
                  <th scope="col">Enroll Status</th>
                  <th scope="col">Gender/Pronouns</th>
                  <th scope="col">Adviser</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Anderson, Andy</td>
                  <td><router-link to="/student/28376465">28376465</router-link></td>
                  <td>afdas</td>
                  <td>afdas</td>
                  <td>asdfads</td>
                  <td>asdfads</td>
                  <td>asdfads</td>
                  <td>Jon Average</td>
                </tr>
                <tr>
                  <td>Thompson, Timmy</td>
                  <td><router-link to="/student/87634323">87634323</router-link></td>
                  <td>asdfads</td>
                  <td>asdfadsf</td>
                  <td>afdas</td>
                  <td>asdfsadfads</td>
                  <td>asdfads</td>
                  <td>April Foolery</td>
                </tr>
                <tr>
                  <td>Johnson, Jill</td>
                  <td><router-link to="/student/29579067">29579067</router-link></td>
                  <td>asdf</td>
                  <td>asda</td>
                  <td>afdas</td>
                  <td>asfd</td>
                  <td>asdfads</td>
                  <td>Bob Samsonite</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <nav aria-label="Page navigation example">
            <ul class="pagination pagination-sm justify-content-end">
              <li class="page-item">
                <a class="page-link" href="#" aria-label="Previous">
                  <span aria-hidden="true">&laquo;</span>
                </a>
              </li>
              <li class="page-item"><a class="page-link" href="#">1</a></li>
              <li class="page-item"><a class="page-link" href="#">2</a></li>
              <li class="page-item"><a class="page-link" href="#">3</a></li>
              <li class="page-item">
                <a class="page-link" href="#" aria-label="Next">
                  <span aria-hidden="true">&raquo;</span>
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from '../layout.vue';

export default {
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: 'Home',
    };
  },
  methods: {},
};
</script>

<style lang="scss"></style>
