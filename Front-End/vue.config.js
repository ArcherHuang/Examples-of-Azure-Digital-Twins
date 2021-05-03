module.exports = {
  devServer: {
    proxy: {
      '/command': {
        changeOrigin: true,
        target: 'https://levanlin-adt-iothub.azure-devices.net',
        pathRewrite: {
          '^/command': '',
        }
      },
      '/map': {
        changeOrigin: true,
        headers: {
          connection: 'keep-alive',
        },
        target: 'https://atlas.microsoft.com',
        pathRewrite: {
          '^/map': '',
        }
      },
    }
  }
}