<template>
  <div>
    <div class="container py-5">
      <NavTabs />
      <v-dialog/>
      <div class="indoor-map">
        <div id="map-id"></div>
      </div>
    </div>
  </div>
</template>

<script>

import NavTabs from '../components/NavTabs.vue';
import twinAPI from '../apis/twin';

const crypto = require('crypto');

export default {
  name: 'Scale',
  data() {
    return {
      map: null,
      center: [-122.13213, 47.63647],
      subscriptionKey: process.env.VUE_APP_MAP_SUBSCRIPTION_KEY,
      tilesetId: process.env.VUE_APP_MAP_TILESETID,
      statesetId: process.env.VUE_APP_MAP_STATESETID,
      parentId: '',
      twinid: '',
      isLoading: false,
      twin: [],
      twinEndName: ['', '', '', ''],
      rpcPrefixName: 'rpc-adt-00',
      endpoint: process.env.VUE_APP_IOT_HUB_ENDPOINT,
      deviceKey: process.env.VUE_APP_IOT_HUB_DEVICEKEY,
      policyName: process.env.VUE_APP_IOT_HUB_POLICYNAME,
      featureId: 0,
      roomName: '',
      deleteRpcId: '',
      deleteParentId: '',
      deleteRelationshipId: '',
    };
  },
  components: {
    NavTabs,
  },
  created() {
    const script = document.createElement('script');
    script.src = 'https://atlas.microsoft.com/sdk/javascript/mapcontrol/2/atlas.min.js';
    script.async = false;
    script.onload = () => {
      console.log('atlas.min.js script is loaded.');
      const script1 = document.createElement('script');
      script1.src = 'https://atlas.microsoft.com/sdk/javascript/indoor/0.1/atlas-indoor.min.js';
      script1.async = false;
      script1.onload = () => {
        console.log('atlas-indoor.min.js script is loaded.');
        this.displayMap();
      };
      document.head.appendChild(script1);
    };
    document.head.appendChild(script);
    const { parentid, twinid } = this.$route.params;
    this.parentId = parentid;
    this.twinid = twinid;
  },
  mounted() {

  },
  methods: {
    getTwinCount(obj, searchString) {
      // eslint-disable-next-line
      for (const k in obj) {
        if (obj[k] instanceof Object) {
          this.getTwinCount(obj[k], searchString);
        } else {
          // eslint-disable-next-line
          if ((obj[k].toString()).startsWith(searchString)) {
            this.twin.push(obj[k]);
            if (searchString === 'rpc-') {
              const tmp = obj[k].split('-');
              console.log(`tmp___tmp: ${tmp}`);
              this.twinEndName[parseInt(tmp[2].replace('00', ''), 10) - 1] = obj[k];
            } else {
              this.twinEndName[parseInt(obj[k].replace('Room-30', ''), 10) - 1] = obj[k];
            }
          }
        }
      }
    },
    async addRpcTwin(rpcId, featureId) {
      this.isLoading = true;
      const addRpcJSON = {
        $metadata: {
          $model: 'dtmi:itri:cms:RPCstat;9',
          kind: 'DigitalTwin',
        },
        threshole5um: 0,
        threshole3um: 0,
        threshole1um: 0,
        threshole05um: 0,
        timetowatch: 0,
        timetosleep: 0,
        rpcAlarm: 0,
        featureId,
      };
      await twinAPI.addRpcTwin(rpcId, addRpcJSON);
      this.isLoading = false;
    },
    async addRoomRpcRelation(roomId, relationshipId, rpcId, relationshipName) {
      const addRoomRpcRelationJSON = {
        $targetId: rpcId,
        $relationshipName: relationshipName,
      };
      await twinAPI.addRoomRpcRelation(
        roomId, relationshipId, addRoomRpcRelationJSON,
      );
    },
    displayMap() {
      this.map = new atlas.Map('map-id', {
        center: this.center,
        language: 'en-US',
        style: 'blank',
        view: 'Auto',
        authOptions: {
          authType: 'subscriptionKey',
          subscriptionKey: this.subscriptionKey,
        },
        zoom: 19,
      });
      const indoorManager = new atlas.indoor.IndoorManager(this.map, {
        levelControl: '',
        tilesetId: this.tilesetId,
        statesetId: this.statesetId,
      });

      if (this.statesetId.length > 0) {
        indoorManager.setDynamicStyling(true);
      }

      this.map.events.add('levelchanged', indoorManager, (eventData) => {
        console.log('The level has changed:', eventData);
      });

      this.map.events.add('facilitychanged', indoorManager, (eventData) => {
        console.log('The facility has changed:', eventData);
      });

      this.map.events.add('click', (e) => {
        const features = this.map.layers.getRenderedShapes(e.position, 'indoor');
        // eslint-disable-next-line
        features.reduce((ids, feature) => {
          if (feature.layer.id === 'indoor_unit_office') {
            this.roomName = feature.properties.name.startsWith(1)
              ? `Room-3${feature.properties.name.slice(-2)}`
              : `Room-${feature.properties.name}`;
            this.featureId = feature.id;
            this.getTwinCount(this.$store.getters.treeJSON, 'rpc-');
            const addRpcName = `${this.rpcPrefixName}${this.twinEndName.indexOf('') + 1}`;
            let action = 'delete';
            const result = this.getNodeFromTree(this.$store.getters.treeJSON, feature.id);
            if (result === null) {
              action = 'add';
            } else {
              this.deleteRpcId = result.name;
              this.deleteParentId = result.parentId;
              this.deleteRelationshipId = result.relationshipId;
            }
            const { title, btns } = this.rpcOps(
              result === null ? addRpcName : result.name,
              this.roomName,
              action,
            );
            this.$modal.show('dialog', {
              title,
              buttons: btns,
            });
          }
        }, []);
      });
    },
    getNodeFromTree(node, featureId) {
      if (node.featureId === featureId) {
        return node;
      // eslint-disable-next-line
      } else if (node.children != null) {
        let result = null;
        for (let i = 0; result == null && i < node.children.length; i += 1) {
          result = this.getNodeFromTree(node.children[i], featureId);
        }
        return result;
      }
      return null;
    },
    rpcOps(rpcId, roomId, action) {
      let btns = [];
      let title = '';
      if (action === 'add') {
        title = `新增 ${rpcId} 到 ${roomId}`;
        btns = [
          {
            title: 'Add RPC',
            handler: () => {
              this.addRPC();
            },
          },
          {
            title: 'Close',
            handler: () => {
              this.$modal.hide('dialog');
            },
          },
        ];
      } else {
        title = `從 ${roomId} 刪除 ${rpcId}`;
        btns = [
          {
            title: 'Delete RPC',
            handler: () => {
              this.deleteRPC();
            },
          },
          {
            title: 'Close',
            handler: () => {
              this.$modal.hide('dialog');
            },
          },
        ];
      }
      return {
        title,
        btns,
      };
    },
    addRPC() {
      const addRpcName = `${this.rpcPrefixName}${this.twinEndName.indexOf('') + 1}`;
      Promise.all([
        this.addRpcTwin(addRpcName, this.featureId),
      ]).then(() => {
        this.addRoomRpcRelation(this.roomName,
          `${this.roomName}_to_${addRpcName}`, addRpcName, 'rpcs');
        const newNode = {
          name: addRpcName,
          parentId: this.roomName,
          relationshipId: `${this.roomName}_to_${addRpcName}`,
          type: 'rpc',
          featureId: this.featureId,
          children: [
            {
              name: '5 um: 0',
            },
            {
              name: '3 um: 0',
            },
            {
              name: '1 um: 0',
            },
            {
              name: '0.5 um: 0',
            },
          ],
        };
        this.insertNodeIntoTree(this.$store.getters.treeJSON,
          this.roomName, newNode);
        this.sendCommandToRpc(this.featureId, addRpcName, 'commandtoadd');
      }).catch((res) => {
        console.error(res);
        this.isLoading = false;
      });
      this.$modal.hide('dialog');
    },
    deleteRPC() {
      this.deleteRpcRelation();
      this.$modal.hide('dialog');
    },
    deleteRpcRelation() {
      Promise.all([
        this.deleteTwinRelationship(this.deleteParentId, this.deleteRelationshipId),
      ]).then(() => {
        this.deleteRpcTwin(this.deleteRpcId);
        this.$store.dispatch('deleteNodeFromTree', {
          node: this.$store.getters.treeJSON,
          nodeName: this.deleteRpcId,
        });
        this.sendCommandToRpc(this.featureId, this.deleteRpcId, 'commandtodelete');
        // this.setRpcColorInMap('no');
      }).catch((res) => {
        console.error(res);
      });
    },
    async deleteTwinRelationship(deleteParentId, deleteRelationshipId) {
      await twinAPI.deleteTwinRelationship(deleteParentId, deleteRelationshipId);
    },
    async deleteRpcTwin(deleteRpcId) {
      await twinAPI.deleteRpcTwin(deleteRpcId);
    },
    chainClosedEvent(val) {
      console.log(`chainClosedEvent: ${val}`);
    },
    insertNodeIntoTree(node, nodeName, newNode) {
      if (node.name === nodeName) {
        if (newNode) {
          node.children.push(newNode);
        }
      } else if (node.children != null) {
        for (let i = 0; i < node.children.length; i += 1) {
          this.insertNodeIntoTree(node.children[i], nodeName, newNode);
        }
      }
    },
    generateSasToken(resourceUri, signingKey, policyName, expiresInMins) {
      // eslint-disable-next-line
      resourceUri = encodeURIComponent(resourceUri);

      // Set expiration in seconds
      let expires = (Date.now() / 1000) + expiresInMins * 60;
      expires = Math.ceil(expires);
      const toSign = `${resourceUri}\n${expires}`;

      // Use crypto
      const hmac = crypto.createHmac('sha256', Buffer.from(signingKey, 'base64'));
      hmac.update(toSign);
      const base64UriEncoded = encodeURIComponent(hmac.digest('base64'));

      // Construct authorization string
      let token = `SharedAccessSignature sr=${resourceUri}&sig=${base64UriEncoded}&se=${expires}`;
      if (policyName) token = `${token}&skn=${policyName}`;
      return token;
    },
    sendCommandToRpc(featureId, rpcId, methodName) {
      // const directMethod = `/command/twins/${rpcId}/methods?api-version=2018-06-30`;
      const directMethod = `https://${this.endpoint}/twins/${rpcId}/methods?api-version=2018-06-30`;
      const token = this.generateSasToken(this.endpoint, this.deviceKey, this.policyName, 360);
      const bodyData = {
        methodName,
        responseTimeoutInSeconds: 200,
        payload: featureId,
      };
      const headers = {
        'Content-Type': 'application/json',
        Authorization: token,
      };
      this.axios.post(directMethod, bodyData, {
        headers,
      }).then((response) => {
        console.log(`response: ${JSON.stringify(response)}`);
      }).catch((error) => {
        console.log(error);
      });
    },
    setRpcColorInMap(colorValue) {
      const featureStateColor = `/map/featureState/state?api-version=1.0&statesetID=${this.statesetId}&featureID=UNIT${this.featureId}&subscription-key=${this.subscriptionKey}`;
      const dateObject = new Date();
      const year = dateObject.getFullYear();
      const month = (dateObject.getMonth() + 1).toString().padStart(2, '0');
      const date = (dateObject.getDate()).toString().padStart(2, '0');
      const hour = (dateObject.getHours()).toString().padStart(2, '0');
      const minute = (dateObject.getMinutes()).toString().padStart(2, '0');
      const second = (dateObject.getSeconds()).toString().padStart(2, '0');
      const bodyData = {
        states: [
          {
            keyName: 'setAlarm',
            value: colorValue,
            eventTimestamp: `${year}-${month}-${date}T${hour}:${minute}:${second}`,
          },
        ],
      };
      const headers = {
        'Content-Type': 'application/json',
      };
      this.axios.post(featureStateColor, bodyData, {
        headers,
      }).then((response) => {
        console.log(`response: ${JSON.stringify(response)}`);
      }).catch((error) => {
        console.log(error);
      });
    },
  },
  beforeDestroy() {

  },
};

</script>

<style>
.indoor-map {
  position: absolute;
  top: 180px;
  left: 350px;
  width: calc(100vw - 350px);
  height: 90%;
}

#map-id {
  width: 70%;
  height: 95%;
}
</style>
