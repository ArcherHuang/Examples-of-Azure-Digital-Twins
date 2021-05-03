<template>
  <div class="container py-5">
    <NavTabs />
    <br />
    <Spinner v-if="isLoading" />
    <template v-else>
      <span class="badge badge-primary model-detail">
        Model ID: {{ this.$route.params.modelId }}
      </span>
      <br/><br/>
      <vue-json-pretty
        :path="'res'"
        :data=modelInfo
        :highlightMouseoverNode=true>
      </vue-json-pretty>
    </template>
  </div>
</template>

<script>

import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
import NavTabs from '../components/NavTabs.vue';
import digitalTwinModelAPI from '../apis/model';
import { Toast } from '../utils/helpers';
import Spinner from '../components/Spinner.vue';

export default {
  name: 'modelView',
  components: {
    NavTabs,
    Spinner,
    VueJsonPretty,
  },
  data() {
    return {
      isLoading: true,
      modelInfo: '',
    };
  },
  created() {
    this.isLoading = true;
    this.getModelById(this.$route.params.modelId);
  },
  methods: {
    async getModelById(modelId) {
      try {
        this.isLoading = true;
        const {
          data: {
            value: [first],
          },
        } = await digitalTwinModelAPI.getModelById(modelId);
        this.modelInfo = first.model;
        this.isLoading = false;
      } catch (error) {
        console.error(error.message);
        this.isLoading = false;
        Toast.fire({
          icon: 'warning',
          title: '無法取得 Model !',
        });
      }
    },
  },
};
</script>
