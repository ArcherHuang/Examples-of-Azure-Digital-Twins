// import LoadScript from 'vue-plugin-load-script';
import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import VTooltip from 'v-tooltip';
import VModal from 'vue-js-modal';
import VueSimpleAlert from 'vue-simple-alert';
import axios from 'axios';
import VueAxios from 'vue-axios';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import './assets/application.css';
// import 'azure-maps-indoor/dist/atlas-indoor.min.css';

Vue.config.productionTip = false;
Vue.use(VueAxios, axios);
Vue.use(VueSimpleAlert);
Vue.use(VTooltip);
Vue.component('font-awesome-icon', FontAwesomeIcon);
library.add(fab, far, fas);
Vue.use(VModal, { dialog: true });
// Vue.use(LoadScript);

// Vue.loadScript('https://atlas.microsoft.com/sdk/javascript/mapcontrol/2/atlas.min.js')
//   .then(() => {
//     console.log('atlas.min.js is loaded');
//   })
//   .catch(() => {
//     console.log('atlas.min.js is Failed');
//   });

// Vue.loadScript('https://atlas.microsoft.com/sdk/javascript/indoor/0.1/atlas-indoor.min.js')
//   .then(() => {
//     console.log('atlas-indoor.min.js is loaded');
//   })
//   .catch(() => {
//     console.log('atlas-indoor.min.js is Failed');
//   });

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
