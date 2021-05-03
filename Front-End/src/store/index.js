import Vue from 'vue';
import Vuex from 'vuex';
import twinAPI from '../apis/twin';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    currentUser: {
      id: -1,
      name: '',
      email: '',
      image: '',
      isAdmin: false,
    },
    connected: false,
    message: '',
    isAuthenticated: false,
    token: '',
    showModal: false,
    modelIdForTwin: null,
    telemetryData: {},
    treeJSON: {
      name: 'Microsoft',
      type: 'company',
      children: [{
        name: '19 樓',
        id: 'F19',
        type: 'floor',
        children: [],
      }],
    },
  },
  getters: {
    telemetryData: (state) => state.telemetryData,
    treeJSON: (state) => state.treeJSON,
  },
  mutations: {
    setshowModal(state, payload) {
      state.showModal = payload;
    },
    setModelIdForTwin(state, payload) {
      state.modelIdForTwin = payload;
    },
    setTreeJSON(state, telemetry) {
      const newNode = {
        name: Object.keys(telemetry)[0],
        children: [
          {
            name: `Count: ${telemetry[Object.keys(telemetry)[0]].count}`,
          },
        ],
      };
      const payload = { node: state.treeJSON, nodeName: Object.keys(telemetry)[0], newNode };
      this.dispatch('updateNodeInTree', payload);
    },
    setTelemetry(state, telemetry) {
      delete state.telemetryData[Object.keys(telemetry)[0]];
      // eslint-disable-next-line
      state.telemetryData = Object.assign({}, state.telemetryData);
      state.telemetryData[Object.keys(telemetry)[0]] = { ...telemetry[Object.keys(telemetry)[0]] };
    },
  },
  actions: {
    // eslint-disable-next-line
    async insertNodeIntoTree({ dispatch }, payload) {
      if (payload.node.name === payload.nodeName) {
        if (payload.newNode) {
          payload.node.children.push(payload.newNode);
        }
      } else if (payload.node.children != null) {
        for (let i = 0; i < payload.node.children.length; i += 1) {
          const tmp = {
            node: payload.node.children[i],
            nodeName: payload.nodeName,
            newNode: payload.newNode,
          };
          dispatch('insertNodeIntoTree', tmp);
        }
      }
    },
    async addFeatureIdInTree({ dispatch }, payload) {
      if (payload.node.name === payload.nodeName) {
        payload.node.featureId = payload.newNode.featureId;
      } else if (payload.node.children != null) {
        for (let i = 0; i < payload.node.children.length; i += 1) {
          const tmp = {
            node: payload.node.children[i],
            nodeName: payload.nodeName,
            newNode: payload.newNode,
          };
          dispatch('addFeatureIdInTree', tmp);
        }
      }
    },
    // eslint-disable-next-line
    async updateNodeInTree({ dispatch, state }, payload) {
      if (payload.node.name === payload.nodeName) {
        // eslint-disable-next-line
        payload.node.children[0].name = payload.newNode.children[0].name;
        // eslint-disable-next-line
        payload.node.children[1].name = payload.newNode.children[1].name;
        // eslint-disable-next-line
        payload.node.children[2].name = payload.newNode.children[2].name;
        // eslint-disable-next-line
        payload.node.children[3].name = payload.newNode.children[3].name;
      } else if (payload.node.children != null) {
        for (let i = 0; i < payload.node.children.length; i += 1) {
          const tmp = {
            node: payload.node.children[i],
            nodeName: payload.nodeName,
            newNode: payload.newNode,
          };
          dispatch('updateNodeInTree', tmp);
        }
      }
    },
    // eslint-disable-next-line
    async deleteNodeFromTree({ dispatch, state }, payload) {
      if (payload.node.children != null) {
        for (let i = 0; i < payload.node.children.length; i += 1) {
          const filtered = payload.node.children.filter((f) => f.name === payload.nodeName);
          if (filtered && filtered.length > 0) {
            // eslint-disable-next-line
            payload.node.children = payload.node.children.filter((f) => f.name !== payload.nodeName);
            return;
          }
          const tmp = {
            node: payload.node.children[i],
            nodeName: payload.nodeName,
          };
          dispatch('deleteNodeFromTree', tmp);
        }
      }
    },
    // eslint-disable-next-line
    async getFeatureIdFromTwin({ state }, twinId) {
      const { data } = await twinAPI.getTwinInfoById(twinId);
      const newNode = {
        name: twinId,
        featureId: data.featureId,
      };
      const payload = { node: state.treeJSON, nodeName: twinId, newNode };
      this.dispatch('addFeatureIdInTree', payload);
    },
    // eslint-disable-next-line
    async checkTwinExist({ commit, dispatch, state }, twinInfo) {
      try {
        await twinAPI.getTwin(twinInfo.name);
        dispatch('getTwinsRelationships', twinInfo.name);
      } catch (error) {
        const addJSON = {
          $metadata: {
            $model: twinInfo.model,
            kind: 'DigitalTwin',
          },
          [twinInfo.keyName]: twinInfo.name,
        };
        await twinAPI.addRpcTwin(twinInfo.name, addJSON);
        Promise.all([
          dispatch('initCreatTwinAndRelation'),
        ]).then(() => {
          dispatch('getTwinsRelationships', 'F19');
        });
      }
    },
    // eslint-disable-next-line
    async initCreatTwinAndRelation({ commit, dispatch, state }) {
      console.log('initCreatTwinAndRelation_initCreatTwinAndRelation');
      const roomJSONInfo = {
        name: 'MPR',
        keyName: 'roomName',
        model: 'dtmi:itri:cms:Room;5',
      };
      const addJSON = {
        $metadata: {
          $model: roomJSONInfo.model,
          kind: 'DigitalTwin',
        },
        [roomJSONInfo.keyName]: roomJSONInfo.name,
      };
      await twinAPI.addRpcTwin(roomJSONInfo.name, addJSON);
      const addtwinRelationJSON = {
        $targetId: 'MPR',
        $relationshipName: 'rooms',
      };
      await twinAPI.addRoomRpcRelation(
        'F19', 'F19_to_MPR', addtwinRelationJSON,
      );
    },
    // eslint-disable-next-line
    async getTwinsRelationships({ commit, dispatch, state }, twinId) {
      try {
        const { data } = await twinAPI.getTwinRelationships(twinId);
        console.log(`getTwinsRelationships__data: ${data}`);
        const promises = [];
        data.value.forEach((child) => {
          console.log(`childchildchild: ${JSON.stringify(child)}`);
          if (child.$relationshipName === 'rooms') {
            const newNode = {
              name: child.$targetId,
              parentId: child.$sourceId,
              relationshipId: child.$relationshipId,
              type: 'room',
              children: [],
            };
            const payload = { node: state.treeJSON, nodeName: '19 樓', newNode };
            dispatch('insertNodeIntoTree', payload);
          } else {
            // eslint-disable-next-line
            const { featureId } = dispatch('getFeatureIdFromTwin', child.$targetId)
            const newNode = {
              name: child.$targetId,
              parentId: child.$sourceId,
              relationshipId: child.$relationshipId,
              type: 'device',
              featureId: '',
              children: [
                {
                  name: 'Count: 0',
                },
              ],
            };
            const payload = { node: state.treeJSON, nodeName: child.$sourceId, newNode };
            dispatch('insertNodeIntoTree', payload);
          }
          promises.push(dispatch('getTwinsRelationships', child.$targetId));
        });
        Promise.all(promises).then(() => {
          console.log(`77777_treeJSON__treeJSON: ${JSON.stringify(state.treeJSON)}`);
        });
      } catch (error) {
        console.error(`222error: ${error.message}`);
      }
    },
  },
  modules: {
  },
});
