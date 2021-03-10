// Run: nodemon index.js / node index.js

// 引入套件
const express = require('express')
const cors = require('cors')

const { DefaultAzureCredential } = require("@azure/identity");
const { createProxyMiddleware } = require('http-proxy-middleware');

if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config()
}

// 使用 express 與設定 port 為 3000
const app = express()
const port = process.env.PORT || 3000

const credential = new DefaultAzureCredential();
let token = null;

app.use(cors())

const pathRewrite = async function (path, req) {
  if (!token || token.expiresOnTimestamp < Date.now()) {
    token = await credential.getToken("https://digitaltwins.azure.net/.default");
  }
  req.headers.authorization = `Bearer ${token.token}`;
  console.log(`token___token: ${token.token}`);
  return path.replace("/api/proxy", "");
};

// Proxy endpoints
app.use(
  '/api/proxy',
  createProxyMiddleware({
    changeOrigin: true,
    headers: {
      connection: "keep-alive"
    },
    target: process.env.AZURE_DIGITAL_TWINS_HOST_NAME,
    onProxyReq: proxyReq => {
      if (proxyReq.getHeader("origin")) {
        proxyReq.removeHeader("origin");
        proxyReq.removeHeader("referer");
      }
    },
    pathRewrite,
  }));

app.listen(port, () => {
  console.log(`Example app listening on port ${port}!`)
})