const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
}
)

// 打包
module.exports = {
  publicPath:'./',  // 执行 npm run build 统一配置路径
}

