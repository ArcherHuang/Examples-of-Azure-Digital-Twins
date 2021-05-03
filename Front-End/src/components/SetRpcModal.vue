<template>
<modal name="set-rpc" transition="pop-out" :width="modalWidth"
  :focus-trap="true" :height="360" @before-open="beforeOpen">
  <div class="box">
    <div class="box-part" id="bp-left">
      <div class="partition">
        <div class="partition-title">Set {{ rpcTwinId }}</div>
        <div class="partition-form">
          <form>
            <div class="lbl-ipt text-center mb-2">
              <label for="5um-threshold">5 um</label>
              <input id="5um-threshold" type="text"
                v-model=threshole5um placeholder="5 um Threshold">
            </div>
            <div class="lbl-ipt text-center">
              <label for="watch-time">Watch Time</label>
              <input id="watch-time" type="text"
                v-model=timetowatch placeholder="Watch Time">
            </div>
          </form>

          <div style="margin-top: 25px"></div>

          <div class="button-set">
            <button id="save-btn" @click="save">Save</button>
            <!-- <button id="cancel-btn" @click="cancel">Cancel</button> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</modal>
</template>

<script>

const MODAL_WIDTH = 500;

export default {
  name: 'SetRpcModal',
  data() {
    return {
      modalWidth: MODAL_WIDTH,
      rpcTwinId: '',
      threshole5um: 0,
      timetowatch: 0,
      // settingChange: [0, 0, 0, 0, 0],
    };
  },
  watch: {

  },
  created() {
    this.modalWidth = window.innerWidth < MODAL_WIDTH ? MODAL_WIDTH / 2 : MODAL_WIDTH;
  },
  methods: {
    save() {
      this.$modal.hide('set-rpc');
      this.$emit('clicked', {
        threshole5um: this.threshole5um,
        timetowatch: this.timetowatch,
      });
    },
    cancel() {
      this.$modal.hide('set-rpc');
    },
    beforeOpen(event) {
      this.threshole5um = event.params.settingValue.threshole5um;
      this.timetowatch = event.params.settingValue.timetowatch;
      this.rpcTwinId = event.params.rpcTwinId;
    },
  },
};
</script>

<style>

.box {
  background: white;
  overflow: hidden;
  width: 656px;
  height: 360px;
  border-radius: 2px;
  box-sizing: border-box;
  box-shadow: 0 0 40px black;
  color: #8b8c8d;
  font-size: 10;
}

.box .box-part {
  display: inline-block;
  position: relative;
  vertical-align: top;
  box-sizing: border-box;
  height: 100%;
  width: 50%;
}

.box .partition .partition-title {
  margin-left: 110px;
  box-sizing: border-box;
  padding: 30px;
  width: 80%;
  text-align: center;
  letter-spacing: 1px;
  font-size: 20px;
  font-weight: 300;
}

.lbl-ipt {
  margin-left: 160px;
}

.box input[type='text'] {
  /* margin-left: 160px; */
  display: block;
  box-sizing: border-box;
  margin-bottom: 4px;
  width: 100%;
  font-size: 12px;
  line-height: 2;
  border: 0;
  border-bottom: 1px solid #dddedf;
  padding: 4px 8px;
  font-family: inherit;
  transition: 0.5s all;
}
.box button {
  margin-left: 180px;
  background: white;
  border-radius: 4px;
  box-sizing: border-box;
  padding: 10px;
  letter-spacing: 1px;
  font-family: 'Open Sans', sans-serif;
  font-weight: 400;
  min-width: 140px;
  margin-top: 8px;
  color: #8b8c8d;
  cursor: pointer;
  border: 1px solid #dddedf;
  text-transform: uppercase;
  transition: 0.1s all;
  font-size: 10px;
}
.box button:hover {
  border-color: #c7c8c9;
  color: #6f7071;
}

.box #cancel-btn {
  margin-left: 8px;
}

.pop-out-enter-active, .pop-out-leave-active {
  transition: all 0.5s;
}
.pop-out-enter, .pop-out-leave-active {
  opacity: 0;
  transform: translateY(24px);
}

</style>
