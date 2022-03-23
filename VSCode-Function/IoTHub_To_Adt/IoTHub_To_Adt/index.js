const { DefaultAzureCredential } = require("@azure/identity");
const axios = require("axios");
require("dotenv").config();

module.exports = async function (context, IoTHubMessages) {
  context.log(
    `JavaScript eventhub trigger function called for message array: ${JSON.stringify(
      IoTHubMessages
    )}`
  );
  context.log(
    `Device ID: ${context.bindingData.systemPropertiesArray[0]["iothub-connection-device-id"]}`
  );

  const credential = new DefaultAzureCredential();
  const token = await credential.getToken(
    "https://digitaltwins.azure.net/.default"
  );

  IoTHubMessages.forEach(async (message, index) => {
    context.log("Processed message: " + JSON.stringify(message));
    const keys = Object.keys(message);
    let request_body = [];
    for (let i = 0; i < keys.length; i++) {
      context.log(keys[i] + ": " + message[keys[i]]);

      request_body.push({
        op: "replace",
        path: `/${keys[i]}`,
        value: message[keys[i]],
      });
    }

    context.log("request_body : " + JSON.stringify(request_body));
    const response = await axios.patch(
      `https://${process.env["ADT_Host"]}/digitaltwins/${context.bindingData.systemPropertiesArray[0]["iothub-connection-device-id"]}?api-version=2020-10-31`,
      request_body,
      {
        headers: {
          Authorization: "Bearer " + token.token,
        },
      }
    );
    context.log("Response: " + JSON.stringify(response));
  });

  context.log("IoTHubMessages: " + JSON.stringify(IoTHubMessages));
};
