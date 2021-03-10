<template>
  <div id="rpc">
    <Navbar />
    <main class="mt-5 bg-white">
      <router-view />
    </main>
  </div>
</template>

<script>

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import Navbar from './components/Navbar.vue';

const { EventHubConsumerClient } = require('@azure/event-hubs');

const connectionString = process.env.VUE_APP_EVENT_HUB_CONNECTIONSTRING;
const eventHubName = process.env.VUE_APP_EVENT_HUB_NAME;
const consumerGroup = '$Default';

export default {
  data() {
    return {
      telemetryData: {},
      treeJSON: {},
    };
  },
  created() {
    this.receiveEventHubData();

    // [
    //   'https://atlas.microsoft.com/sdk/javascript/mapcontrol/2/atlas.min.js',
    //   'https://atlas.microsoft.com/sdk/javascript/indoor/0.1/atlas-indoor.min.js',
    // ].forEach((src) => {
    //   const script = document.createElement('script');
    //   script.src = src;
    //   script.async = false;
    //   document.head.appendChild(script);
    // });
    [
      'https://atlas.microsoft.com/sdk/javascript/mapcontrol/2/atlas.min.css',
      'https://atlas.microsoft.com/sdk/javascript/indoor/0.1/atlas-indoor.min.css',
    ].forEach((src) => {
      const css = document.createElement('link');
      css.setAttribute('rel', 'stylesheet');
      css.setAttribute('href', src);
      css.setAttribute('type', 'text/css');
      css.src = src;
      css.async = false;
      document.head.appendChild(css);
    });
  },
  components: {
    Navbar,
  },
  mounted() {
    this.$store.dispatch('getTwinsRelationships', 'B12-F3');
  },
  methods: {
    async receiveEventHubData() {
      // window.setInterval((() => {
      //   this.treeJSON['rpc-t-1219-001'] = {
      //     '5um': Math.floor(Math.random() * Math.floor(100)),
      //     '3um': Math.floor(Math.random() * Math.floor(100)),
      //     '1um': Math.floor(Math.random() * Math.floor(100)),
      //     '05um': Math.floor(Math.random() * Math.floor(100)),
      //   };
      //   this.$store.commit('setTreeJSON', this.treeJSON);
      // }), 5000);
      const consumerClient = new EventHubConsumerClient(consumerGroup,
        connectionString, eventHubName);
      this.subscription = consumerClient.subscribe({
        processEvents: async (events, context) => {
          events.forEach((event) => {
            this.treeJSON[event.body.$dtId] = {
              '5um': event.body.particle5um,
              '3um': event.body.particle3um,
              '1um': event.body.particle1um,
              '05um': event.body.particle05um,
            };
            this.$store.commit('setTreeJSON', this.treeJSON);
            this.treeJSON = {};
            this.eventData = event.body;
          });
          await context.updateCheckpoint(events[events.length - 1]);
        },
        processError: async (err, context) => {
          console.log(`Error: ${err}, context: ${context}`);
        },
      });
    },
  },
};
</script>

<style scoped>

main {
  margin-top: 65px !important;
}
</style>
