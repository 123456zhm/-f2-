Page({
  data: {
    userInfo: null,
    defaultAvatar: 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQh2jpibhJNpicPZiba6iaaU8GPPlibMia1acPj8S3ic4KbBhpibU5YmJ0Icoib8PW9NA/0',
    userStats: {
      downloads: 0,
      days: 0
    },
    historyCount: 0,
    version: '1.0.0',
    platforms: [],
    settings: {
      notification: true
    },
    cacheSize: '0KB',
    apiConfig: {
      douyin: { api_mode: 'cookie', has_cookie: false, has_api_key: false },
      xiaohongshu: { api_mode: 'cookie', has_cookie: false, has_api_key: false },
      weibo: { has_cookie: false }
    },
    showSettingModal: false,
    currentPlatform: null,
    tempApiKey: '',
    tempCookie: '',
    serverUrl: '',
    faqList: [
      {
        question: '如何使用去水印功能？',
        answer: '复制小红书、抖音或微博的分享链接，粘贴到解析页面，点击解析即可获取无水印内容。',
        expanded: false
      },
      {
        question: '支持哪些平台？',
        answer: '目前支持小红书、抖音、微博三大主流平台，后续会持续增加更多平台。',
        expanded: false
      },
      {
        question: '解析失败怎么办？',
        answer: '请检查链接是否完整，部分内容可能需要登录Cookie才能获取，可尝试使用自动Cookie功能。',
        expanded: false
      },
      {
        question: '下载的内容保存在哪里？',
        answer: '下载的内容会保存在您的手机相册中，同时也会记录在历史记录中方便查看。',
        expanded: false
      }
    ]
  },

  onLoad() {
    this.loadData()
    this.calculateCache()
    this.loadApiConfig()
  },

  onShow() {
    this.updateStats()
  },

  loadData() {
    const app = getApp()
    this.setData({
      platforms: app.globalData.supportedPlatforms,
      historyCount: app.globalData.historyList.length,
      serverUrl: app.globalData.serverUrl
    })
  },

  loadApiConfig() {
    wx.request({
      url: getApp().globalData.serverUrl + '/api/config',
      method: 'GET',
      success: (res) => {
        if (res.data.success) {
          this.setData({ apiConfig: res.data.config })
        }
      },
      fail: (err) => {
        console.error('加载配置失败', err)
      }
    })
  },

  updateStats() {
    const app = getApp()
    const history = app.globalData.historyList
    const downloads = history.length
    const days = Math.floor(downloads / 10) + 1

    this.setData({
      historyCount: history.length,
      userStats: { downloads, days }
    })
  },

  calculateCache() {
    try {
      const res = wx.getStorageInfoSync()
      const sizeKB = res.currentSize
      let sizeText = sizeKB + 'KB'
      if (sizeKB > 1024) {
        sizeText = (sizeKB / 1024).toFixed(2) + 'MB'
      }
      this.setData({ cacheSize: sizeText })
    } catch (e) {
      console.error('获取缓存大小失败', e)
    }
  },

  changeAvatar() {
    wx.getUserProfile({
      desc: '获取用户头像',
      success: (res) => {
        this.setData({
          userInfo: res.userInfo
        })
        wx.showToast({
          title: '登录成功',
          icon: 'success'
        })
      },
      fail: () => {
        wx.showToast({
          title: '取消登录',
          icon: 'none'
        })
      }
    })
  },

  goToHistory() {
    wx.switchTab({
      url: '/pages/history/history'
    })
  },

  goToFeedback() {
    wx.showModal({
      title: '意见反馈',
      content: '如有问题或建议，请联系客服：feedback@example.com',
      showCancel: false
    })
  },

  goToAbout() {
    wx.showModal({
      title: '关于我们',
      content: '免费去水印工具 v1.0.0\n一款免费、高效的去水印下载工具\n支持小红书、抖音、微博等主流平台',
      showCancel: false
    })
  },

  openPlatformSetting(e) {
    const platform = e.currentTarget.dataset.platform
    const config = this.data.apiConfig[platform]
    
    this.setData({
      showSettingModal: true,
      currentPlatform: platform,
      tempApiKey: '',
      tempCookie: ''
    })
  },

  closeSettingModal() {
    this.setData({
      showSettingModal: false,
      currentPlatform: null,
      tempApiKey: '',
      tempCookie: ''
    })
  },

  onApiKeyInput(e) {
    this.setData({ tempApiKey: e.detail.value })
  },

  onCookieInput(e) {
    this.setData({ tempCookie: e.detail.value })
  },

  switchApiMode(e) {
    const mode = e.detail.value ? 'tikhub' : 'cookie'
    const platform = this.data.currentPlatform
    
    wx.request({
      url: getApp().globalData.serverUrl + '/api/config',
      method: 'POST',
      header: { 'Content-Type': 'application/json' },
      data: {
        platform: platform,
        api_mode: mode
      },
      success: (res) => {
        if (res.data.success) {
          wx.showToast({ title: '模式已切换', icon: 'success' })
          this.loadApiConfig()
        }
      },
      fail: (err) => {
        wx.showToast({ title: '切换失败', icon: 'error' })
      }
    })
  },

  saveApiKey() {
    const platform = this.data.currentPlatform
    const apiKey = this.data.tempApiKey
    
    if (!apiKey) {
      wx.showToast({ title: '请输入API Key', icon: 'none' })
      return
    }
    
    wx.request({
      url: getApp().globalData.serverUrl + '/api/config',
      method: 'POST',
      header: { 'Content-Type': 'application/json' },
      data: {
        platform: platform,
        tikhub_api_key: apiKey
      },
      success: (res) => {
        if (res.data.success) {
          wx.showToast({ title: 'API Key已保存', icon: 'success' })
          this.setData({ tempApiKey: '' })
          this.loadApiConfig()
        }
      },
      fail: (err) => {
        wx.showToast({ title: '保存失败', icon: 'error' })
      }
    })
  },

  saveCookie() {
    const platform = this.data.currentPlatform
    const cookie = this.data.tempCookie

    if (!cookie) {
      wx.showToast({ title: '请输入Cookie', icon: 'none' })
      return
    }

    wx.showLoading({ title: '正在优化Cookie...', mask: true })

    wx.request({
      url: getApp().globalData.serverUrl + '/api/cookie/simplify',
      method: 'POST',
      data: {
        platform: platform,
        cookie: cookie
      },
      header: { 'Content-Type': 'application/json' },
      success: (res) => {
        wx.hideLoading()
        if (res.data.success) {
          const originalSize = Math.round(res.data.original_length / 1024 * 10) / 10
          const simplifiedSize = Math.round(res.data.simplified_length / 1024 * 10) / 10
          const savedSize = Math.round((1 - res.data.simplified_length / res.data.original_length) * 100)

          wx.request({
            url: getApp().globalData.serverUrl + '/api/config',
            method: 'POST',
            header: { 'Content-Type': 'application/json' },
            data: {
              platform: platform,
              cookie: res.data.simplified_cookie
            },
            success: (saveRes) => {
              if (saveRes.data.success) {
                wx.showToast({
                  title: `已保存（精简${savedSize}%）`,
                  icon: 'success',
                  duration: 3000
                })
                this.setData({ tempCookie: '' })
                this.loadApiConfig()
              }
            },
            fail: (err) => {
              wx.showToast({ title: '保存失败', icon: 'error' })
            }
          })
        } else {
          wx.showModal({
            title: 'Cookie 优化失败',
            content: '是否直接保存原始Cookie？',
            success: (modalRes) => {
              if (modalRes.confirm) {
                wx.request({
                  url: getApp().globalData.serverUrl + '/api/config',
                  method: 'POST',
                  header: { 'Content-Type': 'application/json' },
                  data: {
                    platform: platform,
                    cookie: cookie
                  },
                  success: (saveRes) => {
                    if (saveRes.data.success) {
                      wx.showToast({ title: '已保存', icon: 'success' })
                      this.setData({ tempCookie: '' })
                      this.loadApiConfig()
                    }
                  }
                })
              }
            }
          })
        }
      },
      fail: (err) => {
        wx.hideLoading()
        wx.showToast({ title: '优化失败', icon: 'error' })
      }
    })
  },

  toggleNotification(e) {
    this.setData({
      'settings.notification': e.detail.value
    })
    wx.showToast({
      title: e.detail.value ? '已开启' : '已关闭',
      icon: 'success'
    })
  },

  editServerUrl() {
    const app = getApp()
    const current = app.globalData.serverUrl
    wx.showModal({
      title: '修改服务器地址',
      content: '真机调试时请改为电脑局域网IP，如 http://192.168.1.100:8000',
      editable: true,
      placeholderText: 'http://192.168.1.100:8000',
      success: (res) => {
        if (res.confirm && res.content) {
          let url = res.content.trim()
          if (url.endsWith('/')) url = url.slice(0, -1)
          app.setServerUrl(url)
          this.setData({ serverUrl: url })
          wx.showToast({ title: '已更新', icon: 'success' })
          console.log('服务器地址已更新:', url)
        }
      }
    })
  },

  clearCache() {
    wx.showModal({
      title: '清除缓存',
      content: '确定要清除所有缓存数据吗？',
      success: (res) => {
        if (res.confirm) {
          try {
            wx.clearStorageSync()
            this.setData({ cacheSize: '0KB' })
            wx.showToast({
              title: '已清除',
              icon: 'success'
            })
          } catch (e) {
            wx.showToast({
              title: '清除失败',
              icon: 'error'
            })
          }
        }
      }
    })
  },

  toggleFaq(e) {
    const index = e.currentTarget.dataset.index
    const faqList = this.data.faqList
    faqList[index].expanded = !faqList[index].expanded
    this.setData({ faqList })
  },

  goToPrivacy() {
    wx.showModal({
      title: '隐私政策',
      content: '我们重视您的隐私保护，所有数据仅存储在本地，不会上传到服务器。',
      showCancel: false
    })
  },

  goToTerms() {
    wx.showModal({
      title: '用户协议',
      content: '本工具仅供个人学习使用，请勿用于商业用途，尊重原创作者版权。',
      showCancel: false
    })
  },

  onShareAppMessage() {
    return {
      title: '免费去水印工具 - 个人中心',
      path: '/pages/profile/profile'
    }
  },

  stopPropagation() {
  }
})