import 'regenerator-runtime/runtime';
import axios from 'axios';

const dataMixin = {
  methods: {
    getStudentList: async function (paginationOptions, searchOptions) {
      const csrfToken = this.$store.state.csrfToken;
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          'Access-Control-Allow-Origin': '*',
          'X-CSRFToken': csrfToken,
        },
      };
      let options = Object.assign({}, paginationOptions, searchOptions);
      return axios.get(
        '/api/internal/student/',
        { params: options },
        axiosConfig
      );
    },
    getStudentDetail: async function (studentNumber) {
      const csrfToken = this.$store.state.csrfToken;
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          'Access-Control-Allow-Origin': '*',
          'X-CSRFToken': csrfToken,
        },
      };
      return axios.get(
        '/api/internal/student/' + studentNumber + '/',
        {},
        axiosConfig
      );
    },
    classesToClassDict(classes) {
      // converts a html class attribute string to a dictionary
      let classDict = {};
      if (classes instanceof String || typeof(classes) === 'string') {
        classes.split(/\s+/).forEach((c) => classDict[c] = true);
      } else if (classes instanceof Array) {
        classes.forEach((c) => classDict[c] = true);
      } else if (classes) {
        // Want to copy here?
        Object.entries(classes).forEach(([key, value]) => classDict[key] = value);
      }
      return classDict;
    }
  },
};

export default dataMixin;
