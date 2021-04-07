<template>
  <div>
    <set-rpc-modal @clicked="saveSettingValue"/>
    <div class="container py-5">
        <NavTabs />
        <Spinner v-if="isLoading" />
        <div class="toolbar-area">
          <div v-show=isEnableToolbar>
            <div class="container text-left mt-5">
              <div class="btn-group fa color">
                <template v-if="toolbarTwinType == 'floor' || toolbarTwinType == 'room'">
                  <button
                    type="button"
                    v-tooltip="tooltipTitle('map')"
                    class="btn btn-outline-secondary btn-sm fa"
                    @click.stop.prevent="openIndoorMap()"
                  >
                    <font-awesome-icon :icon="['fas', 'map-marker-alt']" />
                  </button>
                </template>
                <template v-else>
                  <template v-if="toolbarTwinType == 'rpc'">
                    <button
                      type="button"
                      class="btn btn-outline-secondary btn-sm fa"
                      @click.stop.prevent="settingRPC()"
                      v-tooltip="toolbarTooltipSettingRPC"
                    >
                      <font-awesome-icon :icon="['fas', 'cog']" />
                    </button>
                    <button
                      type="button"
                      v-tooltip="tooltipTitle('map')"
                      class="btn btn-outline-secondary btn-sm fa"
                      @click.stop.prevent="openIndoorMap()"
                    >
                      <font-awesome-icon :icon="['fas', 'map-marker-alt']" />
                    </button>
                  </template>
                </template>
              </div>
            </div>
          </div>
        </div>
        <div id='app-collapse'></div>
    </div>
  </div>
</template>

<script>

import * as d3 from 'd3';
import NavTabs from '../components/NavTabs.vue';
import twinAPI from '../apis/twin';
import Spinner from '../components/Spinner.vue';
import SetRpcModal from '../components/SetRpcModal.vue';

const crypto = require('crypto');

let i = 0;
const duration = 750;

export default {
  name: 'Scale',
  data() {
    return {
      toolbarTooltipDeleteRPC: 'Delete Twin',
      toolbarTooltipSettingRPC: 'Setting RPC',
      toolbarTwinType: '',
      toolbarTwinId: '',
      toolbarParentId: '',
      toolbarRelationshipId: '',
      isLoading: false,
      margin: {
        top: 20,
        right: 90,
        bottom: 30,
        left: 90,
      },
      width: 0,
      height: 0,
      treemap: '',
      svg: '',
      root: '',
      isEnableToolbar: false,
      twin: [],
      twinEndName: ['', '', '', ''],
    };
  },
  components: {
    NavTabs,
    Spinner,
    SetRpcModal,
  },
  created() {
    this.width = 960 - this.margin.left - this.margin.right;
    this.height = 500 - this.margin.top - this.margin.bottom;
  },
  mounted() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters.treeJSON,
      () => {
        this.update(this.$store.getters.treeJSON);
      },
      { deep: true },
    );
    this.drawTree();
  },
  methods: {
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
    saveSettingValue(val) {
      const directMethod = `/command/twins/${this.toolbarTwinId}/methods?api-version=2018-06-30`;
      const endpoint = process.env.VUE_APP_IOT_HUB_ENDPOINT;
      const deviceKey = process.env.VUE_APP_IOT_HUB_DEVICEKEY;
      const policyName = process.env.VUE_APP_IOT_HUB_POLICYNAME;
      const token = this.generateSasToken(endpoint, deviceKey, policyName, 360);
      Object.entries(val).forEach(([key, value]) => {
        let bodyData = {};
        if (key === 'timetowatch') {
          bodyData = {
            methodName: 'settimetowatch',
            responseTimeoutInSeconds: 200,
            payload: value,
          };
        } else {
          bodyData = {
            methodName: key,
            responseTimeoutInSeconds: 200,
            payload: value,
          };
        }
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
      });
    },
    tooltipTitle(action) {
      if (action === 'add') {
        return this.toolbarTwinType === 'floor' ? 'Add Room Twin' : 'Add RPC Twin';
      }
      return action === 'map' ? 'Open Indoor Map' : 'Delete RPC Twin';
    },
    getTwinCount(obj, searchString) {
      // eslint-disable-next-line
      for (const k in obj) {
        if (obj[k] instanceof Object) {
          this.getTwinCount(obj[k], searchString);
        } else {
          // eslint-disable-next-line
          if (obj[k].startsWith(searchString)) {
            this.twin.push(obj[k]);
            if (searchString === 'rpc-') {
              const tmp = obj[k].split('-');
              this.twinEndName[parseInt(tmp[3].replace('00', ''), 10) - 1] = obj[k];
            } else {
              this.twinEndName[parseInt(obj[k].replace('Room-30', ''), 10) - 1] = obj[k];
            }
          }
        }
      }
    },
    addRPC(toolbarTwinType) {
      this.twinEndName = ['', '', '', ''];
      if (toolbarTwinType === 'room') {
        this.getTwinCount(this.$store.getters.treeJSON, 'rpc-');
        const addRpcName = `rpc-adt-00${this.twinEndName.indexOf('') + 3}`;
        Promise.all([
          this.addRpcTwinXY(addRpcName, 0, 0),
        ]).then(() => {
          this.addTwinRelation(this.toolbarTwinId, `${this.toolbarTwinId}_to_${addRpcName}`, addRpcName, 'rpcs');
          const newNode = {
            name: addRpcName,
            parentId: this.toolbarTwinId,
            relationshipId: `${this.toolbarTwinId}_to_${addRpcName}`,
            type: 'rpc',
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
          this.insertNodeIntoTree(this.$store.getters.treeJSON, this.toolbarTwinId, newNode);
        }).catch((res) => {
          console.error(res);
          this.isLoading = false;
        });
      } else if (toolbarTwinType === 'floor') {
        this.getTwinCount(this.$store.getters.treeJSON, 'Room-30');
        const addRpcName = `Room-30${this.twinEndName.indexOf('') + 3}`;
        Promise.all([
          this.addRoomTwinXY(addRpcName),
        ]).then(() => {
          this.addTwinRelation('B12-F3', `B12-F3_to_${addRpcName}`, addRpcName, 'rooms');
          const newNode = {
            name: addRpcName,
            parentId: 'B12-F3',
            relationshipId: `B12-F3_to_${addRpcName}`,
            type: 'room',
            children: [
            ],
          };
          this.insertNodeIntoTree(this.$store.getters.treeJSON, '12 館 3 樓', newNode);
        }).catch((res) => {
          console.error(res);
          this.isLoading = false;
        });
      }
    },
    async addRpcTwinXY(twinId, axisX, axisY) {
      this.isLoading = true;
      await twinAPI.addRpcTwinXY(twinId, axisX, axisY);
      this.isLoading = false;
    },
    async addRoomTwinXY(twinId) {
      this.isLoading = true;
      await twinAPI.addRoomTwinXY(twinId);
      this.isLoading = false;
    },
    async addTwinRelation(parentId, relationshipId, twinId, relationshipName) {
      this.isLoading = true;
      const addTwinRelationJSON = {
        $targetId: twinId,
        $relationshipName: relationshipName,
      };
      await twinAPI.addTwinRelation(parentId, relationshipId, addTwinRelationJSON);
      this.isLoading = false;
    },
    deleteRPC() {
      Promise.all([
        this.deleteTwinRelationship(this.toolbarParentId, this.toolbarRelationshipId),
      ]).then(() => {
        this.deleteTwin(this.toolbarTwinId);
        this.$store.dispatch('deleteNodeFromTree', {
          node: this.$store.getters.treeJSON,
          nodeName: this.toolbarTwinId,
        });
      }).catch((res) => {
        console.error(res);
      });
    },
    async settingRPC() {
      const settingValue = await this.getTwinInfoById(this.toolbarTwinId);
      this.$modal.show('set-rpc', {
        settingValue,
        rpcTwinId: this.toolbarTwinId,
      });
    },
    async getTwinInfoById(twinId) {
      this.isLoading = true;
      const { data } = await twinAPI.getTwinInfoById(twinId);
      this.isLoading = false;
      return {
        threshole5um: data.threshole5um,
        threshole3um: data.threshole3um,
        threshole1um: data.threshole1um,
        threshole05um: data.threshole05um,
        timetowatch: data.timetowatch,
      };
    },
    openIndoorMap() {
      if (typeof this.toolbarParentId === 'undefined') {
        this.toolbarParentId = 'B12-F3';
      }
      window.location.href = `#/indoor-map/${this.toolbarParentId}/${this.toolbarTwinId}`;
    },
    insertNodeIntoTree(node, nodeName, newNode) {
      if (node.name === nodeName) {
        if (newNode) {
          node.children.push(newNode);
        }
      } else if (node.children != null) {
        for (let ii = 0; ii < node.children.length; ii += 1) {
          this.insertNodeIntoTree(node.children[ii], nodeName, newNode);
        }
      }
    },
    async deleteTwinRelationship(parentId, relationId) {
      this.isLoading = true;
      await twinAPI.deleteTwinRelationship(parentId, relationId);
      this.isLoading = false;
    },
    async deleteTwin(markerId) {
      this.isLoading = true;
      await twinAPI.deleteTwin(markerId);
      this.isLoading = false;
    },
    toggle(d) {
      console.log(`click toggle: ${d}`);
    },
    drawTree() {
      this.svg = d3
        .select('#app-collapse')
        .append('svg')
        .attr('id', 'tree')
        .attr('width', this.width + this.margin.right + this.margin.left)
        .attr('height', this.height + this.margin.top + this.margin.bottom)
        .call(d3.zoom().on('zoom', () => {
          console.log('zoom___zoom');
        }))
        .append('g')
        .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
      // declares a tree layout and assigns the size
      this.treemap = d3.tree().size([this.height, this.width]);

      this.root = d3.hierarchy(this.$store.getters.treeJSON, (d) => d.children);
      this.root.x0 = this.height / 2;
      this.root.y0 = 0;
      this.update(this.root);
    },
    collapse(d) {
      if (d.children) {
        d._children = d.children;
        d._children.forEach(this.collapse());
        d.children = null;
      }
    },
    update(source) {
      const treeData1 = this.treemap(this.root);
      const nodes = treeData1.descendants();
      const links = treeData1.descendants().slice(1);
      nodes.forEach((d) => { d.y = d.depth * 180; });
      const node = this.svg.selectAll('g.node')
        // eslint-disable-next-line
        .data(nodes, (d) => { return d.id || (d.id = ++i); });
      const nodeEnter = node.enter().append('g')
        .attr('class', 'node')
        .attr('transform', () => `translate(${source.y0},${source.x0})`)
        .on('click', this.click);
      nodeEnter.append('circle')
        .attr('class', 'node')
        .attr('r', 1e-6)
        .style('fill', (d) => (d._children ? 'lightsteelblue' : '#fff'));
      nodeEnter.append('text')
        .attr('dy', '.35em')
        .attr('x', (d) => (d.children || d._children ? -13 : 13))
        .attr('text-anchor', (d) => (d.children || d._children ? 'end' : 'start'))
        .text((d) => d.data.name);
      const nodeUpdate = nodeEnter.merge(node);
      nodeUpdate.transition()
        .duration(duration)
        .attr('transform', (d) => `translate(${d.y},${d.x})`);
      nodeUpdate.select('circle.node')
        .attr('r', 10)
        .style('fill', (d) => (d._children ? 'lightsteelblue' : '#fff'))
        .attr('cursor', 'pointer');
      const nodeExit = node.exit().transition()
        .duration(duration)
        .attr('transform', () => `translate(${source.y},${source.x})`)
        .remove();
      nodeExit.select('circle')
        .attr('r', 1e-6);
      nodeExit.select('text')
        .style('fill-opacity', 1e-6);
      const link = this.svg.selectAll('path.link')
        .data(links, (d) => d.id);
      const linkEnter = link.enter().insert('path', 'g')
        .attr('class', 'link')
        .attr('d', () => {
          const o = { x: source.x0, y: source.y0 };
          return this.diagonal(o, o);
        });
      const linkUpdate = linkEnter.merge(link);
      linkUpdate.transition()
        .duration(duration)
        .attr('d', (d) => this.diagonal(d, d.parent));
      link.exit().transition()
        .duration(duration)
        .attr('d', () => {
          const o = { x: source.x, y: source.y };
          return this.diagonal(o, o);
        })
        .remove();
      nodes.forEach((d) => {
        d.x0 = d.x;
        d.y0 = d.y;
      });
    },
    diagonal(s, d) {
      const path = `M ${s.y} ${s.x}
          C ${(s.y + d.y) / 2} ${s.x},
            ${(s.y + d.y) / 2} ${d.x},
            ${d.y} ${d.x}`;
      return path;
    },
    click(event, d) {
      if (d.children) {
        d._children = d.children;
        d.children = null;
      } else {
        d.children = d._children;
        d._children = null;
      }
      if (this.toolbarTwinId === d.data.name) {
        this.isEnableToolbar = !this.isEnableToolbar;
      } else {
        this.isEnableToolbar = true;
      }
      this.toolbarTwinType = d.data.type;
      this.toolbarTwinId = d.data.name;
      this.toolbarParentId = d.data.parentId;
      this.toolbarRelationshipId = d.data.relationshipId;
      this.update(d);
    },
  },
  beforeDestroy() {

  },
};

</script>

<style>
.toolbar-area {
  height: 10px;
  border: 1px solid white;
}

.node circle {
  fill: #fff;
  stroke: steelblue;
  stroke-width: 3px;
}

.node text {
  font: 12px sans-serif;
}

.link {
  fill: none;
  stroke: #ccc;
  stroke-width: 2px;
}

.tooltip {
  display: block !important;
  z-index: 10000;
}

.tooltip .tooltip-inner {
  background: black;
  color: white;
  border-radius: 16px;
  padding: 5px 10px 4px;
}

.tooltip .tooltip-arrow {
  width: 0;
  height: 0;
  border-style: solid;
  position: absolute;
  margin: 5px;
  border-color: black;
  z-index: 1;
}

.tooltip[x-placement^="top"] {
  margin-bottom: 5px;
}

.tooltip[x-placement^="top"] .tooltip-arrow {
  border-width: 5px 5px 0 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  bottom: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

.tooltip[x-placement^="bottom"] {
  margin-top: 5px;
}

.tooltip[x-placement^="bottom"] .tooltip-arrow {
  border-width: 0 5px 5px 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-top-color: transparent !important;
  top: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

.tooltip[x-placement^="right"] {
  margin-left: 5px;
}

.tooltip[x-placement^="right"] .tooltip-arrow {
  border-width: 5px 5px 5px 0;
  border-left-color: transparent !important;
  border-top-color: transparent !important;
  border-bottom-color: transparent !important;
  left: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}

.tooltip[x-placement^="left"] {
  margin-right: 5px;
}

.tooltip[x-placement^="left"] .tooltip-arrow {
  border-width: 5px 0 5px 5px;
  border-top-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  right: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}

.tooltip.popover .popover-inner {
  background: #f9f9f9;
  color: black;
  padding: 24px;
  border-radius: 5px;
  box-shadow: 0 5px 30px rgba(black, .1);
}

.tooltip.popover .popover-arrow {
  border-color: #f9f9f9;
}

.tooltip[aria-hidden='true'] {
  visibility: hidden;
  opacity: 0;
  transition: opacity .15s, visibility .15s;
}

.tooltip[aria-hidden='false'] {
  visibility: visible;
  opacity: 1;
  transition: opacity .15s;
}
</style>
