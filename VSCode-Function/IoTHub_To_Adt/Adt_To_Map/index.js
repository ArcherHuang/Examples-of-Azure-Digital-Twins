const { DefaultAzureCredential } = require("@azure/identity");
const axios = require("axios");
require("dotenv").config();

const mapPrimaryKey = process.env["AZURE_MAP_PRIMARY_KEY"];
const statesetId = process.env["STATESET_ID"];

module.exports = async function (context, eventGridEvent) {
  const credential = new DefaultAzureCredential();
  const token = await credential.getToken(
    "https://digitaltwins.azure.net/.default"
  );
  context.log(`token: ${token.token}`);

  const request_body = {
    query: `SELECT * FROM DIGITALTWINS WHERE $dtId = '${eventGridEvent.subject}'`,
  };
  context.log("request_body: " + JSON.stringify(request_body));
  const response = await axios.post(
    `https://${process.env["ADT_Host"]}/query?api-version=2020-10-31`,
    request_body,
    {
      headers: {
        Authorization: "Bearer " + token.token,
      },
    }
  );

  const featureId = JSON.stringify(response.data.value[0].featureId);
  context.log("featureId: " + featureId);

  const keys = Object.keys(response.data.value[0]);
  const twinPropertyThresholdKeys = keys.filter((key) => {
    return key.match(/^threshold/);
  });
  context.log(`twinPropertyThresholdKeys: ${twinPropertyThresholdKeys}`);

  let twinPropertyThreshold = {};
  twinPropertyThresholdKeys.filter((key) => {
    twinPropertyThreshold[key] = response.data.value[0][key];
  });
  context.log(
    `twinPropertyThreshold: ${JSON.stringify(twinPropertyThreshold)}`
  );

  const keyname = "Alarm002";
  context.log("JavaScript Event Grid function processed a request.");
  context.log("ModelId: " + eventGridEvent.subject);
  context.log("Time: " + eventGridEvent.eventTime);
  context.log("Data: " + JSON.stringify(eventGridEvent.data));
  context.log("patch: " + JSON.stringify(eventGridEvent.data.data.patch));

  let isAlarm = false;

  for (
    let index = 0;
    index < eventGridEvent.data.data.patch.length;
    index += 1
  ) {
    // context.log(`op: ${eventGridEvent.data.data.patch[index].op}`);
    context.log(`path: ${eventGridEvent.data.data.patch[index].path}`);
    context.log(`value: ${eventGridEvent.data.data.patch[index].value}`);

    if (!isAlarm) {
      context.log(
        `twinPropertyThreshold: ${JSON.stringify(twinPropertyThreshold)}`
      );
      let threshold =
        twinPropertyThreshold[
          `threshold_${eventGridEvent.data.data.patch[index].path.substring(1)}`
        ];
      context.log(
        `threshold_${eventGridEvent.data.data.patch[index].path.substring(
          1
        )}: ${threshold}`
      );
      context.log(
        ` ${eventGridEvent.data.data.patch[index].path}: ${eventGridEvent.data.data.patch[index].value}`
      );

      if (
        typeof threshold !== "undefined" &&
        eventGridEvent.data.data.patch[index].value > threshold
      ) {
        isAlarm = true;
      }
    }
  }

  let data = {
    states: [
      {
        keyName: keyname,
        value: isAlarm,
        eventTimestamp: getLocalTime(),
      },
    ],
  };

  context.log("2_Request Body: " + JSON.stringify(data));

  axios({
    method: "put",
    url: `https://us.atlas.microsoft.com/featurestatesets/${statesetId}/featureStates/UNIT${featureId}?api-version=2.0&subscription-key=${mapPrimaryKey}`,
    data,
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      context.log("response: " + JSON.stringify(response));
    })
    .catch((error) => {
      context.log("error: " + error);
    });

  context.done();
};

function getLocalTime() {
  const tzoffset = new Date().getTimezoneOffset() * 60000;
  const localISOTime = new Date(Date.now() - tzoffset)
    .toISOString()
    .slice(0, -1);
  console.log(localISOTime);
  return localISOTime;
}
