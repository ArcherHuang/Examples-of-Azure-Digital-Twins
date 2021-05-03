<template>
  <div class="container py-5">
    <NavTabs />
    <h1>Page Not Found</h1>
  </div>
</template>

<script>

import NavTabs from '../components/NavTabs.vue';

export default {
  name: 'not-found',
  components: {
    NavTabs,
  },
  mounted() {
  },
  data() {
    return {
    };
  },
  methods: {
  },
};

</script>
