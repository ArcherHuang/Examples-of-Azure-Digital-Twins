<template>
  <div>
    <set-rpc-modal @clicked="chainClosedEvent"/>
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
                  v-tooltip="tooltipTitle('add')"
                  class="btn btn-outline-secondary btn-sm fa"
                  @click.stop.prevent="addRPC(toolbarTwinType)"
                >
                  <font-awesome-icon :icon="['far', 'plus-square']" />
                </button>
              </template>
              <template v-else>
                <template v-if="toolbarTwinType == 'rpc'">
                  <button
                    type="button"
                    class="btn btn-outline-secondary btn-sm fa"
                    @click.stop.prevent="deleteRPC()"
                    v-tooltip="tooltipTitle('delete')"
                  >
                    <font-awesome-icon :icon="['far', 'trash-alt']" />
                  </button>
                  <button
                    type="button"
                    class="btn btn-outline-secondary btn-sm fa"
                    @click.stop.prevent="settingRPC()"
                    v-tooltip="toolbarTooltipSettingRPC"
                  >
                    <font-awesome-icon :icon="['fas', 'cog']" />
                  </button>
                </template>
              </template>
            </div>
          </div>
        </div>
      </div>
      <div id='app'></div>
    </div>
  </div>
</template>

<script>

import * as d3 from 'd3';
import { mapState } from 'vuex';
import NavTabs from '../components/NavTabs.vue';
import twinAPI from '../apis/twin';
import { Toast } from '../utils/helpers';
import Spinner from '../components/Spinner.vue';
import SetRpcModal from '../components/SetRpcModal.vue';

export default {
  name: 'Graph',
  components: {
    NavTabs,
    Spinner,
    SetRpcModal,
  },
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
        right: 120,
        bottom: 30,
        left: 70,
      },
      width: 0,
      height: 0,
      svg: '',
      isEnableToolbar: false,
      twin: [],
      twinEndName: ['', '', '', ''],
    };
  },
  created() {
    this.width = 700 - this.margin.left - this.margin.right;
    this.height = 600 - this.margin.top - this.margin.bottom;
  },
  mounted() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters.treeJSON,
      () => {
        const svgElment = document.getElementById('tree');
        svgElment.parentNode.removeChild(svgElment);
        this.drawTree();
      },
      { deep: true },
    );
    this.drawTree();
  },
  computed: mapState(['treeJSON']),
  methods: {
    chainClosedEvent(val) {
      console.log(`chainClosedEvent: ${val}`);
    },
    tooltipTitle(action) {
      if (action === 'add') {
        return this.toolbarTwinType === 'floor' ? 'Add Room Twin' : 'Add RPC Twin';
      }
      return 'Delete RPC Twin';
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
        const addRpcName = `rpc-t-1203-00${this.twinEndName.indexOf('') + 3}`;
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
    settingRPC() {
      this.$modal.show('set-rpc', {
        twinId: 'rpc-t-1219-001',
      });
    },
    toggle(d) {
      console.log(`click toggle: ${d}`);
    },
    drawTree() {
      const treemap = d3.tree()
        .size([this.height, this.width]);
      let nodes = d3.hierarchy(this.$store.getters.treeJSON);
      nodes = treemap(nodes);
      // const svg = d3
      this.svg = d3
        .select('#app')
        .append('svg')
        .attr('id', 'tree')
        .attr('width', this.width + this.margin.left + this.margin.right)
        .attr('height', this.height + this.margin.top + this.margin.bottom);
      const view = this.svg
        .append('g')
        .attr('transform', `translate(${this.margin.left},${this.margin.top})`);
      view.selectAll('.link')
        .data(nodes.descendants().slice(1))
        .enter().append('path')
        .attr('class', 'link')
        // eslint-disable-next-line
        .attr('d', (d) => 'M' + d.y + ',' + d.x
            + 'C' + (d.y + d.parent.y) / 2 + ',' + d.x
            + ' ' + (d.y + d.parent.y) / 2 + ',' + d.parent.x
            + ' ' + d.parent.y + ',' + d.parent.x);
      const node = view.selectAll('.node')
        .data(nodes.descendants())
        .enter().append('g')
        .on('click', (event, d) => {
          if (this.toolbarTwinId === d.data.name) {
            this.isEnableToolbar = !this.isEnableToolbar;
          } else {
            this.isEnableToolbar = true;
          }
          this.toolbarTwinType = d.data.type;
          this.toolbarTwinId = d.data.name;
          this.toolbarParentId = d.data.parentId;
          this.toolbarRelationshipId = d.data.relationshipId;
        })
        // eslint-disable-next-line
        .attr('class', (d) => 'node' + (d.children ? ' node--internal' : ' node--leaf'))
        .attr('transform', (d) => `translate(${d.y},${d.x})`);
      node.append('circle')
        .attr('r', 10);
      node.append('text')
        .attr('dy', '.35em')
        .attr('y', (d) => (d.children ? -20 : 1))
        .attr('x', (d) => (d.children ? 1 : 55))
        .style('text-anchor', 'middle')
        .text((d) => d.data.name);
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
    async getTwinsRelationships(twinId) {
      try {
        this.isLoading = true;
        const { data } = await twinAPI.getTwinRelationships(twinId);
        const promises = [];
        data.value.forEach((child) => {
          if (child.$relationshipName === 'rooms') {
            const newNode = {
              name: child.$targetId,
              parentId: child.$sourceId,
              relationshipId: child.$relationshipId,
              children: [],
            };
            this.insertNodeIntoTree(this.treeJSON, '12 館 3 樓', newNode);
          } else {
            const newNode = {
              name: child.$targetId,
              parentId: child.$sourceId,
              relationshipId: child.$relationshipId,
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
            this.insertNodeIntoTree(this.treeJSON, child.$sourceId, newNode);
          }
          promises.push(this.getTwinsRelationships(child.$targetId));
        });
        Promise.all(promises).then(() => {
          console.log(`22_treeJSON__treeJSON: ${JSON.stringify(this.treeJSON)}`);
        });
        this.isLoading = false;
      } catch (error) {
        console.error(error.message);
        this.isLoading = false;
        Toast.fire({
          icon: 'warning',
          title: '無法取得 Relationships !',
        });
      }
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

.node--internal text {
  text-shadow: 0 1px 0 #fff, 0 -1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff;
}

.link {
  fill: none;
  stroke: #ccc;
  stroke-width: 2px;
}

.fa {
  font-size: 18px;
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
