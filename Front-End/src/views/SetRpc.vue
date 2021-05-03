<template>
  <div class="container py-5">
    <NavTabs />
    <router-link :to="{
      name: 'indoor',
      params: {
        floorId,
      }
      }" class="btn btn-outline-danger mb-4">Back to Indoor Map</router-link>
    <template>
      <div class="row">
        <AlarmCard
          :is-processing="isProcessing"
          :device-id="deviceId"
          @after-submit="handleAfterSubmit"
        />
      </div>
    </template>
  </div>
</template>
<script>

import { Toast } from '../utils/helpers';
// import Spinner from '../components/Spinner.vue';
import NavTabs from '../components/NavTabs.vue';
import AlarmCard from '../components/RpcAlarm.vue';

export default {
  name: 'Sets',
  components: {
    NavTabs,
    AlarmCard,
    // Spinner,
  },
  data() {
    return {
      isProcessing: false,
      isLoading: true,
      deviceId: '',
      floorId: '',
    };
  },
  created() {
  },
  mounted() {
    const { deviceid } = this.$route.params;
    const { floorid } = this.$route.params;
    this.deviceId = deviceid;
    this.floorId = floorid;
  },
  methods: {
    async handleAfterSubmit() {
      try {
        this.isProcessing = true;
        this.isProcessing = false;
      } catch (error) {
        this.isProcessing = false;
        Toast.fire({
          icon: 'error',
          title: '無法更新 RPC Alarm 資料，請稍後再試',
        });
      }
    },
  },
};
</script>
