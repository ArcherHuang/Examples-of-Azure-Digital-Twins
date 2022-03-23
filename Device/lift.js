require("dotenv").config();
const Protocol = require("azure-iot-device-mqtt").Mqtt;
const Client = require("azure-iot-device").Client;
const Message = require("azure-iot-device").Message;

let deviceConnectionString =
  process.env.LIFT001_IOT_HUB_DEVICE_CONNECTION_STRING;

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
          SV02: getRandomArbitrary(50, 100),
          SI01: getRandomArbitrary(1, 40),
          upTime: getRandomArbitrary(1, 40),
          machineSpeed: getRandomArbitrary(1, 40),
          machineActivation: getRandomArbitrary(1, 40),
          orderNum: getRandomArbitrary(1, 40),
        })
      );
      
      console.log(`SP01 (壓力 Sensor): ${JSON.parse(msg.data).SP01}`);
      console.log(`ST01 (溫度 Sensor): ${JSON.parse(msg.data).ST01}`);
      console.log(
        `machineActivation (生產傢動率): ${
          JSON.parse(msg.data).machineActivation
        }`
      );
      console.log(`orderNum (生產數量): ${JSON.parse(msg.data).orderNum}`);
      console.log(
        `machineSpeed (生產運轉速率): ${JSON.parse(msg.data).machineSpeed}`
      );
      console.log(`upTime (運轉總時間): ${JSON.parse(msg.data).upTime}`);
      console.log(`SV02 (電壓 Sensor): ${JSON.parse(msg.data).SV02}`);
      console.log(`SI01 (電流 Sensor): ${JSON.parse(msg.data).SI01}`);
      
      msg.contentType = "application/json";
      msg.contentEncoding = "utf-8";
      await client.sendEvent(msg);
      await sleep(60000);
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
