import Vue from 'vue';
import VueRouter from 'vue-router';
import NotFound from '../views/NotFound.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'root',
    redirect: '/model',
  },
  {
    path: '/map',
    name: 'map',
    component: () => import('../views/Map.vue'),
  },
  {
    path: '/graph',
    name: 'graph',
    component: () => import('../views/Graph.vue'),
  },
  {
    path: '/collapse',
    name: 'collapse',
    component: () => import('../views/Collapse.vue'),
  },
  {
    path: '/indoor-map/:parentid/:twinid',
    name: 'AzureIndoorMap',
    component: () => import('../views/AzureIndoorMap.vue'),
  },
  {
    path: '/model/add',
    name: 'addModel',
    component: () => import('../views/ModelAdd.vue'),
  },
  {
    path: '/model/view',
    name: 'modelView',
    component: () => import('../views/ModelView.vue'),
  },
  {
    path: '/model',
    name: 'model',
    component: () => import('../views/Model.vue'),
  },
  {
    path: '/set/:floorid/:deviceid',
    name: 'setRpc',
    component: () => import('../views/SetRpc.vue'),
  },
  {
    path: '*',
    name: 'not-found',
    component: NotFound,
  },
];

const router = new VueRouter({
  linkExactActiveClass: 'active',
  routes,
});

export default router;
