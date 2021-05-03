<template>
  <div class="container py-5">
    <NavTabs />
    <router-link :to="{
      name: 'addModel',
      params: {
          role: 'admin'
        }
      }" class="btn btn-outline-danger mb-4">Upload Model</router-link>
    <Spinner v-if="isLoading" />
    <table v-else class="table">
      <thead class="thead-dark">
        <tr>
          <th class="text-center" scope="col">Model ID</th>
          <th class="text-center" scope="col">Display Name</th>
          <th class="text-center" scope="col">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="model in models" :key="model.id" class="hover-table">
          <td class="position-relative text-center">
            <div class="model-id pt-2">{{ model.id }}</div>
          </td>
          <td class="position-relative text-center">
            <div class="model-displayName pt-2">{{ model.displayName.en }}</div>
          </td>
          <td class="text-center">
            <router-link :to="{
              name: 'modelView',
              params: {
                  modelId: model.id
                }
              }" class="btn btn-outline-primary mr-2">View Model</router-link>
            <button
              type="button"
              class="btn btn-outline-primary mr-2"
              @click.stop.prevent="deleteModel(model.id)"
            >Delete Model</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>

import digitalTwinModelAPI from '../apis/model';
import twinAPI from '../apis/twin';
import { Toast } from '../utils/helpers';
import NavTabs from '../components/NavTabs.vue';
import Spinner from '../components/Spinner.vue';

export default {
  name: 'model',
  components: {
    NavTabs,
    Spinner,
  },
  data() {
    return {
      isLoading: true,
      models: [],
    };
  },
  computed: {
    showModal: {
      get() {
        return this.$store.state.showModal;
      },
      set(value) {
        this.$store.commit('setshowModal', value);
      },
    },
    modelIdForTwin: {
      get() {
        return this.$store.state.modelIdForTwin;
      },
      set(value) {
        this.$store.commit('setModelIdForTwin', value);
      },
    },
  },
  mounted() {
  },
  created() {
    this.getListModel();
  },
  methods: {
    async getListModel() {
      try {
        this.isLoading = true;
        const { data } = await digitalTwinModelAPI.listModel();
        this.models = data.value;
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
    async deleteModel(modelId) {
      try {
        this.isLoading = true;
        await digitalTwinModelAPI.deleteModel(modelId);
        this.models = this.models.filter(
          (models) => models.id !== modelId,
        );

        Toast.fire({
          icon: 'success',
          title: '成功刪除 Model',
        });
        this.isLoading = false;
      } catch (error) {
        console.error(error.message);
        this.isLoading = false;
        Toast.fire({
          icon: 'error',
          title: '無法刪除 Model，請稍後再試',
        });
      }
    },
    createTwin(modelId) {
      try {
        this.$prompt("Input twin's name")
          .then((text) => {
            this.addTwin(text, modelId);
          })
          .catch(() => console.log('canceled'));
      } catch (error) {
        console.error(error.message);
      }
    },
    async addTwin(twinName, modelId) {
      try {
        this.isLoading = true;
        const addTwinJSON = {
          $metadata: {
            $model: modelId,
          },
        };
        await twinAPI.addTwin(twinName, addTwinJSON);

        Toast.fire({
          icon: 'success',
          title: '成功新增 Twin',
        });
        this.isLoading = false;
      } catch (error) {
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
