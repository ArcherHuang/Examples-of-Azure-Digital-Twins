import { apiHelper } from '../utils/helpers';

export default {
  listModel() {
    return apiHelper.get('/api/proxy/models?api-version=2020-10-31');
  },
  deleteModel(modelId) {
    return apiHelper.delete(`/api/proxy/models/${modelId}?api-version=2020-10-31`);
  },
  getModelById(modelId) {
    return apiHelper.get(`/api/proxy/models/${modelId}?api-version=2020-10-31`);
  },
  addModel(modelInfo) {
    return apiHelper.post('/api/proxy/models?api-version=2020-10-31',
      `
    [
      ${modelInfo}
    ]
    `);
  },
};
