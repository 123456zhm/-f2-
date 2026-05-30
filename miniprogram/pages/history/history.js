Page({
  data: {
    historyList: [],
    totalCount: 0,
    todayCount: 0,
    videoCount: 0,
    // 详情弹窗相关
    showDetail: false,
    currentDetail: null,
    // 视频播放器相关
    showVideoPlayer: false,
    currentVideoUrl: '',
    currentVideoTitle: ''
  },

  onLoad() {
    this.loadHistory()
  },

  onShow() {
    this.loadHistory()
  },

  loadHistory() {
    const app = getApp()
    const list = app.globalData.historyList || []

    const today = new Date().toDateString()
    const todayCount = list.filter(item => new Date(item.time).toDateString() === today).length
    const videoCount = list.filter(item => item.type === 'video').length

    list.forEach(item => {
      if (!item.platformIcon && item.platform) {
        if (item.platform.key) {
          item.platformIcon = item.platform.icon
          item.platformKey = item.platform.key
        } else if (typeof item.platform === 'string') {
          const platforms = app.globalData.supportedPlatforms
          const platform = platforms.find(p => p.key === item.platform)
          if (platform) {
            item.platformIcon = platform.icon
            item.platformKey = platform.key
          }
        }
      }

      if (!item.author && item.platform && item.platform.name) {
        item.author = item.platform.name
      }
      
      // 确保 fileCount 正确计算
      if (!item.fileCount) {
        const imageCount = (item.images && Array.isArray(item.images)) ? item.images.length : 0
        const videoCount = (item.videoUrl) ? 1 : 0
        item.fileCount = imageCount + videoCount
      }
    })

    this.setData({
      historyList: list,
      totalCount: list.length,
      todayCount,
      videoCount
    })
  },

  // 查看详情
  viewDetail(e) {
    const item = e.currentTarget.dataset.item
    if (!item) {
      wx.showToast({ title: '数据异常', icon: 'none' })
      return
    }
    
    console.log('查看详情:', item)
    
    this.setData({
      showDetail: true,
      currentDetail: item
    })
  },

  // 关闭详情
  closeDetail() {
    this.setData({
      showDetail: false,
      currentDetail: null
    })
  },

  stopPropagation() {
    // 阻止事件冒泡
  },

  // 预览图片
  previewImage(e) {
    const url = e.currentTarget.dataset.url
    const images = e.currentTarget.dataset.images || (this.data.currentDetail?.images || [url])
    
    if (!url || url === 'undefined' || url === 'null') {
      wx.showToast({ title: '图片加载失败', icon: 'none' })
      return
    }

    wx.previewImage({
      current: url,
      urls: images.filter(img => img && img !== 'undefined' && img !== 'null')
    })
  },

  // 播放视频（通过后端代理避免403）
  playVideo() {
    const detail = this.data.currentDetail
    if (!detail || !detail.videoUrl) {
      wx.showToast({ title: '视频链接不存在', icon: 'none' })
      return
    }

    // 通过后端流式接口代理播放，添加 Referer 头避免403
    const streamUrl = getApp().globalData.serverUrl + '/api/stream?url=' + encodeURIComponent(detail.videoUrl)

    this.setData({
      showVideoPlayer: true,
      currentVideoUrl: streamUrl,
      currentVideoTitle: detail.title || '视频预览'
    })
    
    console.log('打开视频播放器(代理):', detail.videoUrl.substring(0, 80) + '...')
  },

  // 关闭视频播放器
  closeVideoPlayer() {
    this.setData({
      showVideoPlayer: false,
      currentVideoUrl: '',
      currentVideoTitle: ''
    })
  },

  onVideoError(e) {
    console.error('视频播放失败:', e.detail.errMsg)
    wx.showToast({ title: '视频播放失败，链接可能已失效', icon: 'none', duration: 2000 })
    this.closeVideoPlayer()
  },

  onVideoEnded(e) {
    console.log('视频播放结束')
    wx.showToast({ title: '播放结束', icon: 'none' })
  },

  // 从详情弹窗下载视频
  downloadFromDetail() {
    const detail = this.data.currentDetail
    if (detail && detail.videoUrl) {
      this.downloadVideo(detail.videoUrl, detail.title || '视频')
    }
  },

  // 从详情弹窗下载图片
  downloadImagesFromDetail() {
    const detail = this.data.currentDetail
    if (detail && detail.images && detail.images.length > 0) {
      this.downloadImages(detail.images, detail.title || '图片')
    }
  },

  // 重新解析
  reParse() {
    const detail = this.data.currentDetail
    if (!detail || !detail.url) {
      wx.showToast({ title: '原始链接不存在', icon: 'none' })
      return
    }

    this.closeDetail()

    // 跳转到解析页面重新解析
    wx.setStorageSync('pendingRedownloadUrl', detail.url)
    wx.setStorageSync('pendingRedownloadPlatform', detail.platformKey || detail.platform?.key || 'xiaohongshu')
    wx.navigateTo({
      url: '/pages/parse/parse?redownload=1'
    })
  },

  previewMedia(e) {
    const item = e.currentTarget.dataset.item
    // 改为打开详情弹窗
    this.viewDetail(e)
  },

  reDownload(e) {
    const item = e.currentTarget.dataset.item

    if (!item) {
      wx.showToast({
        title: '数据异常',
        icon: 'none'
      })
      return
    }

    console.log('重新下载历史记录:', item)

    if (item.type === 'video' && item.videoUrl) {
      this.downloadVideo(item.videoUrl, item.title || '视频')
    } else if (item.type === 'note' && item.images && item.images.length > 0) {
      this.downloadImages(item.images, item.title || '图片')
    } else if (item.images && item.images.length > 0) {
      this.downloadImages(item.images, item.title || '图片')
    } else if (item.url) {
      wx.showModal({
        title: '⚠️ 链接已失效',
        content: '视频链接已过期，无法直接下载\n\n请选择操作：',
        showCancel: true,
        confirmText: '重新解析',
        cancelText: '取消',
        success: (res) => {
          if (res.confirm) {
            wx.setStorageSync('pendingRedownloadUrl', item.url)
            wx.setStorageSync('pendingRedownloadPlatform', item.platform?.key || 'douyin')
            wx.navigateTo({
              url: '/pages/parse/parse?redownload=1'
            })
          }
        }
      })
    } else {
      wx.showModal({
        title: '❌ 下载失败',
        content: '历史记录中未保存下载链接\n\n可能原因：\n1. 这是旧版本保存的记录\n2. 解析时未成功获取视频地址\n\n建议：删除此记录，重新解析下载',
        showCancel: true,
        confirmText: '删除记录',
        cancelText: '保留',
        success: (res) => {
          if (res.confirm) {
            this.deleteItem({ currentTarget: { dataset: { id: item.id } } })
          }
        }
      })
    }
  },

  downloadVideo(videoUrl, title) {
    wx.showLoading({ title: '正在下载视频...\n请耐心等待', mask: true })

    const that = this
    const fileName = `${title}_${Date.now()}.mp4`

    wx.downloadFile({
      url: videoUrl,
      filePath: wx.env.USER_DATA_PATH + '/' + fileName,
      timeout: 120000,

      success: function(downloadRes) {
        wx.hideLoading()

        if (downloadRes.statusCode === 200) {
          wx.saveVideoToPhotosAlbum({
            filePath: downloadRes.filePath,
            success: function(saveRes) {
              wx.showToast({
                title: '视频已保存到相册',
                icon: 'success',
                duration: 3000
              })
            },
            fail: function(saveErr) {
              if (saveErr.errMsg && saveErr.errMsg.includes('auth deny')) {
                wx.showModal({
                  title: '⚠️ 权限不足',
                  content: '需要授权保存视频到相册\n\n请按以下步骤操作：\n1. 点击"确定"打开设置\n2. 找到"保存到相册"权限\n3. 开启权限后重试',
                  showCancel: true,
                  confirmText: '去设置',
                  success: function(res) {
                    if (res.confirm) {
                      wx.openSetting()
                    }
                  }
                })
              } else {
                wx.showToast({
                  title: '保存失败: ' + (saveErr.errMsg || '未知错误'),
                  icon: 'none',
                  duration: 4000
                })
              }
            }
          })
        } else {
          wx.showToast({
            title: `下载失败: HTTP ${downloadRes.statusCode}`,
            icon: 'none',
            duration: 4000
          })
        }
      },

      fail: function(err) {
        wx.hideLoading()

        let errorMsg = '下载失败'
        if (err.errMsg) {
          if (err.errMsg.includes('timeout') || err.errMsg.includes('Timeout')) {
            errorMsg = '⏰ 下载超时\n视频较大，请检查网络后重试'
          } else if (err.errMsg.includes('abort')) {
            errorMsg = '下载被中断，请重试'
          } else if (err.errMsg.includes('network')) {
            errorMsg = '网络连接失败，请检查网络'
          } else if (err.errMsg.includes('invalid')) {
            errorMsg = '视频链接已失效'
          }
        }

        wx.showModal({
          title: '下载失败',
          content: errorMsg + '\n\n提示：视频链接可能已失效',
          showCancel: true,
          confirmText: '重试',
          cancelText: '取消',
          success: function(res) {
            if (res.confirm) {
              that.downloadVideo(videoUrl, title)
            }
          }
        })
      }
    })
  },

  downloadImages(images, title) {
    if (!images || images.length === 0) {
      wx.showToast({
        title: '没有可下载的图片',
        icon: 'none'
      })
      return
    }

    wx.showLoading({ title: `正在下载 ${images.length} 张图片...\n请耐心等待`, mask: true })

    let successCount = 0
    let failCount = 0
    let currentIndex = 0
    const total = images.length

    const updateProgress = () => {
      currentIndex++
      wx.showLoading({
        title: `正在下载 ${currentIndex}/${total}\n成功: ${successCount} 失败: ${failCount}`,
        mask: true,
        duration: 10000
      })
    }

    const checkComplete = () => {
      if (successCount + failCount === total) {
        wx.hideLoading()

        if (failCount === 0) {
          wx.showToast({
            title: `✅ 全部下载成功 (${successCount})`,
            icon: 'success',
            duration: 3000
          })
        } else {
          wx.showModal({
            title: '📊 下载完成',
            content: `成功: ${successCount} 张\n失败: ${failCount} 张\n\n失败原因可能是图片链接失效或网络问题`,
            showCancel: false,
            confirmText: '知道了'
          })
        }
      }
    }

    const downloadNext = (index) => {
      if (index >= total) {
        checkComplete()
        return
      }

      const imageUrl = images[index]
      const fileName = `${title}_${index + 1}_${Date.now()}.jpg`

      wx.downloadFile({
        url: imageUrl,
        filePath: wx.env.USER_DATA_PATH + '/' + fileName,
        timeout: 60000,

        success: function(downloadRes) {
          if (downloadRes.statusCode === 200) {
            wx.saveImageToPhotosAlbum({
              filePath: downloadRes.filePath,
              success: function() {
                successCount++
                updateProgress()
                downloadNext(index + 1)
              },
              fail: function() {
                failCount++
                updateProgress()
                downloadNext(index + 1)
              }
            })
          } else {
            failCount++
            updateProgress()
            downloadNext(index + 1)
          }
        },

        fail: function() {
          failCount++
          updateProgress()
          downloadNext(index + 1)
        }
      })
    }

    downloadNext(0)
  },

  deleteItem(e) {
    const id = e.currentTarget.dataset.id
    wx.showModal({
      title: '确认删除',
      content: '是否删除此记录？',
      success: (res) => {
        if (res.confirm) {
          const newList = this.data.historyList.filter(item => item.id !== id)
          const app = getApp()
          app.globalData.historyList = newList
          wx.setStorageSync('downloadHistory', JSON.stringify(newList))
          this.loadHistory()
          wx.showToast({
            title: '已删除',
            icon: 'success'
          })
        }
      }
    })
  },

  clearAllHistory() {
    wx.showModal({
      title: '确认清空',
      content: '是否清空所有历史记录？',
      success: (res) => {
        if (res.confirm) {
          const app = getApp()
          app.clearHistory()
          this.setData({
            historyList: [],
            totalCount: 0,
            todayCount: 0,
            videoCount: 0
          })
          wx.showToast({
            title: '已清空',
            icon: 'success'
          })
        }
      }
    })
  },

  goToParse() {
    wx.navigateTo({
      url: '/pages/parse/parse'
    })
  }
})