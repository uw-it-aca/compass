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
    }
  },
};

export default dataMixin;
