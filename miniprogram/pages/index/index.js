Page({
  data: {
    platforms: [],
    stats: {
      totalDownloads: '10万+',
      todayDownloads: '1.2万'
    },
    historyCount: 0,
    tutorialSteps: [
      { title: '复制分享链接', desc: '在小红薯/抖海/围脖中复制分享链接' },
      { title: '粘贴解析', desc: '将链接粘贴到输入框，点击解析按钮' },
      { title: '下载保存', desc: '选择需要的内容，点击下载保存到手机' }
    ]
  },

  onLoad() {
    this.loadData()
  },

  onShow() {
    this.updateHistoryCount()
  },

  loadData() {
    const app = getApp()
    this.setData({
      platforms: app.globalData.supportedPlatforms
    })
  },

  updateHistoryCount() {
    const app = getApp()
    this.setData({
      historyCount: app.globalData.historyList.length
    })
  },

  selectPlatform(e) {
    const platform = e.currentTarget.dataset.platform
    wx.showToast({
      title: `${platform.name}已支持`,
      icon: 'success'
    })
  },

  goToParse() {
    wx.navigateTo({
      url: '/pages/parse/parse'
    })
  },

  goToHistory() {
    wx.switchTab({
      url: '/pages/history/history'
    })
  },

  goToProfile() {
    wx.switchTab({
      url: '/pages/profile/profile'
    })
  },

  onShareAppMessage() {
    return {
      title: '免费去水印工具 - 一键解析下载',
      path: '/pages/index/index',
      imageUrl: ''
    }
  }
})