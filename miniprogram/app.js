App({
  globalData: {
    userInfo: null,
    historyList: [],
    // 服务器地址 - 真机调试时改为电脑局域网IP，如 http://192.168.1.100:8000
    // 开发者工具中可用 http://localhost:8000
    serverUrl: 'http://10.170.48.43:8000',
    supportedPlatforms: [
      { name: '小红薯', key: 'xiaohongshu', color: '#ff2442', icon: '📕' },
      { name: '抖海', key: 'douyin', color: '#161823', icon: '🎵' },
      { name: '围脖', key: 'weibo', color: '#ff8200', icon: '📱' }
    ]
  },

  onLaunch() {
    this.loadHistory()
    this.loadServerUrl()
    this.checkUpdate()
  },

  loadServerUrl() {
    try {
      const saved = wx.getStorageSync('serverUrl')
      if (saved) {
        this.globalData.serverUrl = saved
        console.log('使用自定义服务器地址:', saved)
      }
    } catch (e) {
      console.error('加载服务器地址失败', e)
    }
  },

  setServerUrl(url) {
    this.globalData.serverUrl = url
    wx.setStorageSync('serverUrl', url)
  },

  loadHistory() {
    try {
      const history = wx.getStorageSync('downloadHistory')
      if (history) {
        this.globalData.historyList = JSON.parse(history)
      }
    } catch (e) {
      console.error('加载历史记录失败', e)
    }
  },

  saveHistory(item) {
    try {
      this.globalData.historyList.unshift(item)
      if (this.globalData.historyList.length > 100) {
        this.globalData.historyList = this.globalData.historyList.slice(0, 100)
      }
      wx.setStorageSync('downloadHistory', JSON.stringify(this.globalData.historyList))
    } catch (e) {
      console.error('保存历史记录失败', e)
    }
  },

  clearHistory() {
    try {
      this.globalData.historyList = []
      wx.removeStorageSync('downloadHistory')
    } catch (e) {
      console.error('清除历史记录失败', e)
    }
  },

  checkUpdate() {
    if (wx.canIUse('getUpdateManager')) {
      const updateManager = wx.getUpdateManager()
      updateManager.onCheckForUpdate((res) => {
        if (res.hasUpdate) {
          updateManager.onUpdateReady(() => {
            wx.showModal({
              title: '更新提示',
              content: '新版本已经准备好，是否重启应用？',
              success: (res) => {
                if (res.confirm) {
                  updateManager.applyUpdate()
                }
              }
            })
          })
        }
      })
    }
  }
})