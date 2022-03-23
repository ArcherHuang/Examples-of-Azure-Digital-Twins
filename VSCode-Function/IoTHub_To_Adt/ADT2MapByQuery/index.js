const { DefaultAzureCredential } = require("@azure/identity");
const axios = require("axios");
require("dotenv").config();

module.exports = async function (context, req) {
  const query = req.body.query;
  const credential = new DefaultAzureCredential();
  let token = null;
  token = await credential.getToken("https://digitaltwins.azure.net/.default");
  console.log(`Token: ${token.token}`);
  console.log(`getAdtqueryInfo: ${JSON.stringify(query)}`);

  const request_body = {
    query: query,
  };
  const response = await axios.post(
    `https://${process.env["ADT_Host"]}/query?api-version=2020-10-31`,
    request_body,
    {
      headers: {
        Authorization: "Bearer " + token.token,
      },
    }
  );
  context.res = {
    status: 200,
    body: response.data,
  };
};
