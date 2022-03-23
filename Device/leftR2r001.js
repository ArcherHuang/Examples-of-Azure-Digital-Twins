require("dotenv").config();
const Protocol = require("azure-iot-device-mqtt").Mqtt;
const Client = require("azure-iot-device").Client;
const Message = require("azure-iot-device").Message;

let deviceConnectionString =
  process.env.LEFT_R2R001_IOT_HUB_DEVICE_CONNECTION_STRING;

const sleep = (ms) => {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
};

function getRandomArbitrary(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}

async function main() {
  const client = Client.fromConnectionString(deviceConnectionString, Protocol);

  try {
    await client.open();
    while (true) {
      const msg = new Message(
        JSON.stringify({
          SP01: getRandomArbitrary(1, 40),
          ST01: getRandomArbitrary(1, 40),
          SV01: getRandomArbitrary(1, 12),
          SV02: getRandomArbitrary(50, 100),
          SI01: getRandomArbitrary(1, 40),
          SC01: getRandomArbitrary(1, 40),
          SA01: getRandomArbitrary(1, 40),
          SA02: getRandomArbitrary(1, 40),
          SA03: getRandomArbitrary(1, 40),
          upTime: getRandomArbitrary(1, 40),
          machineSpeed: getRandomArbitrary(1, 40),
          machineActivation: getRandomArbitrary(1, 40),
          orderNum: getRandomArbitrary(1, 40),
        })
      );
      console.log(`SP01 (壓力 Sensor): ${JSON.parse(msg.data).SP01}`);
      console.log(`ST01 (溫度 Sensor): ${JSON.parse(msg.data).ST01}`);
      console.log(
        `SV01 (電壓 Sensor (0V ~ 12V)): ${JSON.parse(msg.data).SV01}`
      );
      console.log(
        `SV02 (電壓 Sensor (50V ~ 100V)): ${JSON.parse(msg.data).SV02}`
      );
      console.log(`SI01 (電流 Sensor): ${JSON.parse(msg.data).SI01}`);
      console.log(`SC01 (粒子 Sensor): ${JSON.parse(msg.data).SC01}`);
      console.log(`SA01 (x 軸加速 Sensor): ${JSON.parse(msg.data).SA01}`);
      console.log(`SA02 (y 軸加速 Sensor): ${JSON.parse(msg.data).SA02}`);
      console.log(`SA03 (z 軸加速 Sensor): ${JSON.parse(msg.data).SA03}`);
      console.log(`upTime (運轉總時間): ${JSON.parse(msg.data).upTime}`);
      console.log(
        `machineSpeed (生產運轉速率): ${JSON.parse(msg.data).machineSpeed}`
      );
      console.log(
        `machineActivation (生產傢動率): ${
          JSON.parse(msg.data).machineActivation
        }`
      );
      console.log(`orderNum (生產數量): ${JSON.parse(msg.data).orderNum}`);
      msg.contentType = "application/json";
      msg.contentEncoding = "utf-8";
      await client.sendEvent(msg);
      await sleep(10000);
    }
  } catch (err) {
    console.error(
      "could not connect Plug and Play client or could not attach interval function for telemetry\n" +
        err.toString()
    );
  }
}

main()
  .then(() => console.log("executed sample"))
  .catch((err) => console.log("error", err));
