<template>
  <div class="col-md-6 col-lg-6 text-center">
    <div class="card mb-4 rpc-card">
      <div class="card-header">
        <p class="card-text text-truncate">{{ deviceId }}</p>
      </div>
      <div class="card-body pt-3">
        <form class="coloffset-lg-3 text-center mt-3" @submit.stop.prevent="handleSubmit">
          <div class="form-group">
            <div class="container">
              <div class="row">
                <div class="col">
                  <label for="fiveMicrometerAlarm">5 µm</label>
                  <input
                    id="fiveMicrometerAlarm"
                    type="number"
                    class="form-control"
                    name="fiveMicrometerAlarm"
                    placeholder="Enter 5 µm Alarm"
                    maxlength="7"
                    min="0"
                    max="2999999"
                  />
                </div>
                <div class="col">
                  <label for="watchTime">T1 ( Watch time )</label>
                  <input
                    id="watchTime"
                    type="number"
                    class="form-control"
                    name="watchTime"
                    placeholder="Enter Watch time"
                    maxlength="3"
                    min="10"
                    max="1000"
                  />
                </div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <div class="container">
              <div class="row">
                <div class="col">
                  <label for="threeMicrometerAlarm">3 µm</label>
                  <input
                    id="threeMicrometerAlarm"
                    type="number"
                    class="form-control"
                    name="threeMicrometerAlarm"
                    placeholder="Enter 3 µm Alarm"
                    maxlength="7"
                    min="0"
                    max="2999999"
                  />
                </div>
                <div class="col">
                  <label for="sleepTime">T2 ( Sleep time )</label>
                  <input
                    id="sleepTime"
                    type="number"
                    class="form-control"
                    name="sleepTime"
                    placeholder="Enter Sleep time"
                    maxlength="3"
                    min="1"
                    max="360"
                  />
                </div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <div class="container">
              <div class="row">
                <div class="col">
                  <label for="oneMicrometerAlarm">1 µm</label>
                  <input
                    id="oneMicrometerAlarm"
                    type="number"
                    class="form-control"
                    name="oneMicrometerAlarm"
                    placeholder="Enter 1 µm Alarm"
                    maxlength="7"
                    min="0"
                    max="2999999"
                  />
                </div>
                <div class="col"></div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <div class="container">
              <div class="row">
                <div class="col">
                  <label for="zeroPointFiveMicrometerAlarm">0.5 µm</label>
                  <input
                    id="zeroPointFiveMicrometerAlarm"
                    type="number"
                    class="form-control"
                    name="zeroPointFiveMicrometerAlarm"
                    placeholder="Enter 0.5 µm Alarm"
                    maxlength="7"
                    min="0"
                    max="2999999"
                  />
                </div>
                <div class="col"></div>
              </div>
            </div>
          </div>
          <div class="form-group">
            <div class="container">
              <div class="row">
                <div class="col">
                  <label for="zeroPointThreeMicrometerAlarm">0.3 µm</label>
                  <input
                    id="zeroPointThreeMicrometerAlarm"
                    type="number"
                    class="form-control"
                    name="zeroPointThreeMicrometerAlarm"
                    placeholder="Enter 0.3 µm Alarm"
                    maxlength="7"
                    min="0"
                    max="2999999"
                  />
                </div>
                <div class="col"></div>
              </div>
            </div>
          </div>
          <button
            type="submit"
            class="btn btn-danger"
            :disabled="isProcessing"
          >{{ isProcessing ? '處理中' : '送出' }}</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  components: {

  },
  props: {
    isProcessing: {
      type: Boolean,
      default: false,
    },
    deviceId: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
    };
  },
  watch: {
  },
  methods: {
    handleSubmit() {
    },
  },
};
</script>
