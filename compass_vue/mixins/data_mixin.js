import 'regenerator-runtime/runtime';
import axios from 'axios';

const dataMixin = {
  methods: {
    getEnrolledStudentsList: async function (filters) {
      const csrfToken = this.$store.state.csrfToken;
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8',
          'Access-Control-Allow-Origin': '*',
          'X-CSRFToken': csrfToken,
        },
      };
      return axios.post(
        `/api/internal/edw/enrolled-students/`,
        filters,
        axiosConfig
      );
    },
  },
};

export default dataMixin;
