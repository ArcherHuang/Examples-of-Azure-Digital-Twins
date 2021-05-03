<template>
  <div class="container py-5">
    <NavTabs />
    Model Upload
    <br/>
    <br/>
    <div class="custom-file">
      <input type="file" class="custom-file-input"
      id="file" ref="file" v-on:change="handleFileUpload()" required>
      <label class="custom-file-label" for="file">Choose model file...</label>
      <br/><br/>
      <button v-on:click="submitFile()" class="btn btn-outline-primary mr-2">Submit</button>
    </div>
  </div>
</template>

<script>

import NavTabs from '../components/NavTabs.vue';
import { Toast } from '../utils/helpers';
import digitalTwinModelAPI from '../apis/model';

export default {
  name: 'model',
  components: {
    NavTabs,
  },
  data() {
    return {
      file: '',
    };
  },
  methods: {
    handleFileUpload() {
      [this.file] = this.$refs.file.files;
    },
    submitFile() {
      const formData = new FormData();
      formData.append('file', this.file);
      const reader = new FileReader();
      reader.readAsText(this.file);
      reader.onload = (event) => {
        const fileAsText = event.target.result;
        this.addModel(fileAsText);
      };
    },
    async addModel(modelInfo) {
      try {
        await digitalTwinModelAPI.addModel(modelInfo);
        Toast.fire({
          icon: 'success',
          title: '成功新增 Twin',
        });
        this.isLoading = false;
        this.$router.push({ name: 'model' });
      } catch (error) {
        console.error(error);
        console.error(error.message);
        this.isLoading = false;
        Toast.fire({
          icon: 'error',
          title: '無法新增 Twin，請稍後再試',
        });
      }
    },
  },
};

</script>
