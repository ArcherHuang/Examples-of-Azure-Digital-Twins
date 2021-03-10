<template>
  <ul class="nav nav-tabs mb-4">
    <li v-for="tab in tabs" :key="tab.id" class="nav-item">
      <template v-if="currentUser.role == 'admin'">
        <router-link :to="tab.path" class="nav-link nav-element">{{ tab.title }}</router-link>
      </template>
      <template v-else>
        <template v-if="validated(tab.path)">
          <router-link :to="tab.path" class="nav-link">{{ tab.title }}</router-link>
        </template>
      </template>
    </li>
  </ul>
</template>

<script>
import { mapState } from 'vuex';
import uuid from 'uuid/v4';

export default {
  data() {
    return {
      tabs: [
        {
          id: uuid(),
          title: 'DTDL',
          path: '/model',
        },
        {
          id: uuid(),
          title: 'Outdoor Map',
          path: '/map',
        },
        {
          id: uuid(),
          title: 'Tree Graph',
          path: '/collapse',
        },
      ],
    };
  },
  computed: {
    ...mapState(['currentUser']),
  },
  methods: {
    validated(tabPath) {
      if (tabPath === '/logs/itri') {
        return false;
      }
      return true;
    },
  },
};
</script>

<style scoped>
.nav-tabs {
  border-bottom: 1px solid #bd2333;
}
.nav-link {
  color:  #bd2333;
}
.nav-tabs .nav-link:focus,
.nav-tabs .nav-link:hover,
.nav-tabs .nav-item.show .nav-link,
.nav-tabs .nav-link.active {
  border-color: #bd2333;
  background-color: #bd2333;
  color: white;
}
</style>
