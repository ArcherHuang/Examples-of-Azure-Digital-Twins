<template>
  <nav class="navbar navbar-expand-lg fixed-top navbar-dark bg-dark">
    <router-link class="navbar-brand" to="/">Azure Percept - Digital Twins</router-link>

    <button
      class="navbar-toggler"
      type="button"
      data-toggle="collapse"
      data-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon" />
    </button>

    <div id="navbarSupportedContent" class="navbar-collapse collapse">
      <div class="ml-auto d-flex align-items-center">
        <template v-if="isAuthenticated">
          <div class="text-white mr-3">{{ currentUser.account || '使用者' }} 您好</div>
          <button
            type="button"
            class="btn btn-sm btn-outline-dark my-2 my-sm-0 btnlogout"
            @click="logout"
          >登出</button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState(['currentUser', 'isAuthenticated']),
  },
  methods: {
    logout() {
      this.$store.commit('revokeAuthentication');
      this.$router.push('/signin');
    },
  },
};
</script>

<style scoped>
.navbar-toggler {
  min-width: 70px;
  margin-right: 0;
}
nav.bg-dark {
  padding: 14px 16px;
  background-color: #bd2333 !important;
}
.navbar-brand {
  font-size: 19px;
  padding: 0;
}
</style>
