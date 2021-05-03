<template>
  <div class="container py-5">
    <NavTabs />
    <div class="outdoor-map">
      <div id="map"></div>
    </div>
  </div>
</template>

<script>

import * as atlas from 'azure-maps-control';
import NavTabs from '../components/NavTabs.vue';

export default {
  name: 'Map',
  components: {
    NavTabs,
  },
  data() {
    return {
      subscriptionKey: process.env.VUE_APP_MAP_SUBSCRIPTION_KEY,
      mapCenter: [parseFloat(process.env.VUE_APP_LONGITUDE),
        parseFloat(process.env.VUE_APP_LATITUDE)],
      mapText: process.env.VUE_APP_COMPANY_NAME,
      contextMenu: '',
      map: '',
      zoom: 12,
    };
  },
  created() {
  },
  mounted() {
    this.initMap();
  },
  methods: {
    async initMap() {
      // eslint-disable-next-line
      this.map = new atlas.Map('map', {
        center: this.mapCenter,
        zoom: this.zoom,
        view: 'Auto',
        language: 'en-US',
        // language: 'zh-HanT;zh-TW',
        authOptions: {
          authType: 'subscriptionKey',
          subscriptionKey: this.subscriptionKey,
        },
      });
      this.map.controls.add(new atlas.control.ZoomControl(), {
        position: 'top-right',
      });
      await this.buildMap();
    },
    buildMap() {
      const self = this;
      self.map.events.add('ready', () => {
        const marker = new atlas.HtmlMarker({
          htmlContent: '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="30" height="37" viewBox="0 0 30 37" xml:space="preserve"><rect x="0" y="0" rx="8" ry="8" width="30" height="30" fill="{color}"/><polygon fill="{color}" points="10,29 20,29 15,37 10,29"/><text x="15" y="20" style="font-size:16px;font-family:arial;fill:#ffffff;" text-anchor="middle">{text}</text></svg>',
          color: 'Blue',
          text: this.mapText,
          position: this.mapCenter,
        });

        self.map.markers.add(marker);

        self.map.events.add('click', marker, () => {
          window.location.href = '#/indoor-map/F19/19 樓';
        });
      });
    },
  },
  beforeDestroy() {
  },
};
</script>

<style>
.outdoor-map {
  position: absolute;
  top: 180px;
  left: 350px;
  width: calc(100vw - 350px);
  height: 90%;
}

#map {
  width: 70%;
  height: 70%;
}

.contextMenu {
  border: 1px solid gray;
  min-width: 125px;
  list-style: none;
  display: block;
  list-style-position: outside;
  list-style-type: none;
  margin: 0;
  padding: 0;
}

.contextMenu li {
  cursor: pointer;
  display: block;
  padding: 6px 12px;
}

.contextMenu li:focus,
.contextMenu li:hover {
  background-color: rgba(0, 0, 0, .05);
}

.contextMenu a,
.contextMenu a:hover,
.contextMenu a:focus,
.contextMenu a:active {
  text-decoration: none;
  color: black;
  font-size: 14px;
}
</style>
