import axios from 'axios';
import Swal from 'sweetalert2';

// const baseURL = 'https://rpc-digitaltwins-api.azurewebsites.net';
const baseURL = 'http://localhost:3000';

const axiosInstance = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
});

axiosInstance.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    const vmConfig = config;

    if (token) {
      vmConfig.headers.Authorization = `Bearer ${token}`;
    }

    return vmConfig;
  },
  (err) => Promise.reject(err),
);

export const apiHelper = axiosInstance;

export const Toast = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 3000,
});
