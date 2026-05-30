Page({
  data: {
    linkUrl: '',
    detectedPlatform: null,
    isParsing: false,
    parseResult: null,
    errorMsg: '',
    errorTips: [],
    recentLinks: [],
    showVideoPlayer: false,
    currentVideoUrl: '',
    currentVideoTitle: ''
  },

  onLoad(options) {
    this.loadRecentLinks()

    if (options && options.redownload === '1') {
      const pendingUrl = wx.getStorageSync('pendingRedownloadUrl')
      const pendingPlatform = wx.getStorageSync('pendingRedownloadPlatform')

      if (pendingUrl) {
        wx.removeStorageSync('pendingRedownloadUrl')
        wx.removeStorageSync('pendingRedownloadPlatform')

        setTimeout(() => {
          this.setData({ linkUrl: pendingUrl })
          this.detectPlatform(pendingUrl)

          if (pendingPlatform) {
            const app = getApp()
            const platforms = app.globalData.supportedPlatforms
            const platform = platforms.find(p => p.key === pendingPlatform)
            if (platform) {
              this.setData({ detectedPlatform: platform })
            }
          }

          setTimeout(() => {
            this.parseLink()
          }, 500)
        }, 100)
      }
    }
  },

  loadRecentLinks() {
    try {
      const recent = wx.getStorageSync('recentLinks') || []
      this.setData({ recentLinks: recent.slice(0, 5) })
    } catch (e) {
      console.error('加载最近解析失败', e)
    }
  },

  onInputChange(e) {
    const value = e.detail.value.trim()
    this.setData({ linkUrl: value })
    this.detectPlatform(value)
  },

  detectPlatform(url) {
    if (!url) {
      this.setData({ detectedPlatform: null })
      return
    }

    const app = getApp()
    const platforms = app.globalData.supportedPlatforms

    if (url.includes('xiaohongshu') || url.includes('xhslink') || url.includes('xiaohongshu.com')) {
      this.setData({ detectedPlatform: platforms[0] })
    } else if (url.includes('douyin') || url.includes('dytt') || url.includes('amemv.com')) {
      this.setData({ detectedPlatform: platforms[1] })
    } else if (url.includes('weibo') || url.includes('weibo.com')) {
      this.setData({ detectedPlatform: platforms[2] })
    } else {
      this.setData({ detectedPlatform: null })
    }
  },

  pasteFromClipboard() {
    wx.getClipboardData({
      success: (res) => {
        const text = res.data.trim()
        this.setData({ linkUrl: text })
        this.detectPlatform(text)
        wx.showToast({
          title: '已粘贴',
          icon: 'success'
        })
      },
      fail: () => {
        wx.showToast({
          title: '粘贴失败',
          icon: 'error'
        })
      }
    })
  },

  clearInput() {
    this.setData({
      linkUrl: '',
      detectedPlatform: null,
      parseResult: null,
      errorMsg: ''
    })
  },

  parseLink() {
    if (!this.data.linkUrl) {
      wx.showToast({
        title: '请输入链接',
        icon: 'none'
      })
      return
    }

    if (!this.data.detectedPlatform) {
      this.setData({
        errorMsg: '无法识别链接平台',
        errorTips: ['链接格式不正确', '不支持该平台', '请检查链接是否完整']
      })
      return
    }

    this.setData({
      isParsing: true,
      parseResult: null,
      errorMsg: ''
    })

    wx.showLoading({ title: '解析中...', mask: true })

    this.callParseAPI()
  },

  callParseAPI() {
    const that = this
    wx.request({
      url: getApp().globalData.serverUrl + '/api/parse',
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      data: {
        url: this.data.linkUrl,
        platform: this.data.detectedPlatform.key
      },
      timeout: 60000, // 60秒超时

      success: function(res) {
        wx.hideLoading()
        if (res.statusCode === 200 && res.data.success) {
          that.setData({
            isParsing: false,
            parseResult: res.data
          })
          that.saveToRecent()
          that.saveToHistory(res.data)
          wx.showToast({
            title: '解析成功',
            icon: 'success'
          })
        } else {
          let errorMsg = res.data.detail || res.data.error || '解析失败'
          let errorTips = ['服务器返回错误', '请稍后重试']

          if (errorMsg.includes('无法获取视频下载地址')) {
            errorTips = [
              '视频已被删除或设为私密',
              '视频链接已过期',
              '请尝试重新获取抖海分享链接'
            ]
          } else if (errorMsg.includes('超时') || errorMsg.includes('Timeout')) {
            errorTips = [
              '⏰ API解析超时',
              '可能原因：',
              '1. TikHub服务器响应慢',
              '2. 网络不稳定',
              '3. 请稍后重试'
            ]
          } else if (errorMsg.includes('API') || errorMsg.includes('api')) {
            errorTips = [
              'API服务暂时不可用',
              '请稍后重试',
              '或检查API配置'
            ]
          } else if (errorMsg.includes('连接')) {
            errorTips = [
              '无法连接到服务器',
              '请检查后端服务是否运行',
              '检查网络连接'
            ]
          }

          that.setData({
            isParsing: false,
            errorMsg: errorMsg,
            errorTips: errorTips
          })

          wx.showModal({
            title: '❌ 解析失败',
            content: errorMsg + '\n\n' + errorTips.join('\n'),
            showCancel: true,
            confirmText: '重试',
            cancelText: '取消',
            success: function(modalRes) {
              if (modalRes.confirm) {
                console.log('用户点击重试')
                that.parseLink()
              }
            }
          })
        }
      },
      fail: function(err) {
        wx.hideLoading()
        console.error('API调用失败', err)

        let errorMsg = '网络连接失败'
        let errorTips = ['请检查网络连接', '服务暂时不可用', '请稍后重试']

        if (err.errMsg) {
          if (err.errMsg.includes('timeout') || err.errMsg.includes('Timeout')) {
            errorMsg = '⏰ 请求超时\n\n60秒内未收到服务器响应'
            errorTips = [
              '可能原因：',
              '1. 网络连接不稳定',
              '2. 后端服务响应过慢',
              '3. TikHub API超时',
              '',
              '请稍后重试'
            ]
          } else if (err.errMsg.includes('abort')) {
            errorMsg = '❌ 请求被中断'
            errorTips = ['请稍后重试', '检查网络连接']
          } else if (err.errMsg.includes('network') || err.errMsg.includes('Network')) {
            errorMsg = '🌐 网络连接失败'
            errorTips = ['请检查WiFi或移动网络', '确保设备已联网']
          } else if (err.errMsg.includes('refused') || err.errMsg.includes('refuse')) {
            errorMsg = '🔌 服务器拒绝连接'
            errorTips = ['后端服务可能未启动', '请检查服务是否正常运行']
          }
        }

        that.setData({
          isParsing: false,
          errorMsg: errorMsg,
          errorTips: errorTips
        })

        wx.showModal({
          title: '❌ 网络错误',
          content: errorMsg + '\n\n' + errorTips.join('\n'),
          showCancel: true,
          confirmText: '重试',
          cancelText: '取消',
          success: function(modalRes) {
            if (modalRes.confirm) {
              console.log('用户点击重试')
              that.parseLink()
            }
          }
        })
      }
    })
  },

  saveToRecent() {
    try {
      let recent = wx.getStorageSync('recentLinks') || []
      const newItem = {
        id: Date.now(),
        url: this.data.linkUrl,
        platform: this.data.detectedPlatform.key,
        icon: this.data.detectedPlatform.icon,
        time: new Date().toLocaleTimeString()
      }

      recent = recent.filter(item => item.url !== this.data.linkUrl)
      recent.unshift(newItem)
      recent = recent.slice(0, 10)

      wx.setStorageSync('recentLinks', recent)
      this.setData({ recentLinks: recent.slice(0, 5) })
    } catch (e) {
      console.error('保存最近解析失败', e)
    }
  },

  saveToHistory(result) {
    const app = getApp()
    const historyItem = {
      id: Date.now(),
      platform: this.data.detectedPlatform,
      platformIcon: this.data.detectedPlatform?.icon || '',
      platformKey: this.data.detectedPlatform?.key || '',
      title: result.title || '无标题',
      cover: result.cover || (result.images && result.images.length > 0 ? result.images[0] : ''),
      type: result.type || 'video',
      url: this.data.linkUrl,
      time: new Date().toLocaleString(),
      status: 'success',
      // 视频相关
      videoUrl: result.videoUrl || result.downloadUrl || '',
      // 图片列表 - 确保完整保存
      images: result.images || [],
      // 作者信息
      author: result.author || '',
      // 描述信息
      desc: result.desc || '',
      // 互动数据
      likes: result.likes || result.likeCount || 0,
      comments: result.comments || result.commentCount || 0,
      shares: result.shares || result.shareCount || 0,
      // 文件计数
      fileCount: (result.images ? result.images.length : 0) + (result.videoUrl || result.downloadUrl ? 1 : 0)
    }
    
    console.log('保存到历史记录:', {
      title: historyItem.title,
      type: historyItem.type,
      imageCount: historyItem.images.length,
      hasVideo: !!historyItem.videoUrl,
      hasCover: !!historyItem.cover
    })
    
    app.saveHistory(historyItem)
  },

  useRecentLink(e) {
    const link = e.currentTarget.dataset.link
    this.setData({ linkUrl: link })
    this.detectPlatform(link)
  },

  previewImage(e) {
    const url = e.currentTarget.dataset.url
    const images = this.data.parseResult?.images || [url]

    if (!url || url === 'undefined' || url === 'null') {
      wx.showToast({
        title: '图片加载失败',
        icon: 'none'
      })
      return
    }

    wx.previewImage({
      current: url,
      urls: images.filter(img => img && img !== 'undefined' && img !== 'null')
    })
  },

  onCoverImageError: function(e) {
    console.error('封面图片加载失败:', e)
    this.setData({
      'parseResult.cover': null
    })
    wx.showToast({
      title: '封面图片加载失败',
      icon: 'none',
      duration: 2000
    })
  },

  playVideo() {
    if (!this.data.parseResult || !this.data.parseResult.videoUrl) {
      wx.showToast({
        title: '视频链接不存在',
        icon: 'none'
      })
      return
    }

    const videoUrl = this.data.parseResult.videoUrl
    const title = this.data.parseResult.title || '视频预览'

    // 通过后端流式接口代理播放，添加 Referer 头避免403
    const streamUrl = getApp().globalData.serverUrl + '/api/stream?url=' + encodeURIComponent(videoUrl)

    this.setData({
      showVideoPlayer: true,
      currentVideoUrl: streamUrl,
      currentVideoTitle: title
    })

    console.log('打开视频播放器(代理):', videoUrl.substring(0, 80) + '...')
  },

  closeVideoPlayer() {
    this.setData({
      showVideoPlayer: false,
      currentVideoUrl: '',
      currentVideoTitle: ''
    })
  },

  onVideoError(e) {
    console.error('视频播放失败:', e.detail.errMsg)
    wx.showToast({
      title: '视频播放失败',
      icon: 'none'
    })
    this.closeVideoPlayer()
  },

  onVideoEnded(e) {
    console.log('视频播放结束')
    wx.showToast({
      title: '播放结束',
      icon: 'none'
    })
  },

  stopPropagation() {
    // 阻止事件冒泡，防止点击播放器时关闭
  },

  downloadAll() {
    if (!this.data.parseResult) {
      wx.showToast({
        title: '请先解析链接',
        icon: 'none'
      })
      return
    }

    const result = this.data.parseResult

    if (result.type === 'video' && result.videoUrl) {
      this.downloadVideo(result.videoUrl, result.title || '视频')
    } else if (result.images && result.images.length > 0) {
      this.downloadImages(result.images, result.title || '图片')
    } else {
      wx.showToast({
        title: '没有可下载的内容',
        icon: 'none'
      })
    }
  },

  downloadSingle(e) {
    const type = e.currentTarget.dataset.type
    const url = e.currentTarget.dataset.url
    const title = e.currentTarget.dataset.title || '文件'

    if (type === 'video') {
      this.downloadVideo(url, title)
    } else if (type === 'image') {
      this.downloadImage(url, title)
    }
  },

  downloadVideo(videoUrl, title) {
    wx.showLoading({ title: '正在下载视频...\n请耐心等待', mask: true })

    const that = this
    const fileName = `${title}_${Date.now()}.mp4`

    wx.downloadFile({
      url: videoUrl,
      filePath: wx.env.USER_DATA_PATH + '/' + fileName,
      timeout: 120000, // 2分钟超时

      success: function(downloadRes) {
        wx.hideLoading()

        if (downloadRes.statusCode === 200) {
          console.log('视频下载完成，正在保存到相册...')

          wx.saveVideoToPhotosAlbum({
            filePath: downloadRes.filePath,
            success: function(saveRes) {
              wx.showToast({
                title: '视频已保存到相册',
                icon: 'success',
                duration: 3000
              })
              console.log('视频保存成功:', saveRes)
            },
            fail: function(saveErr) {
              console.error('保存视频失败:', saveErr)

              if (saveErr.errMsg && saveErr.errMsg.includes('auth deny')) {
                wx.showModal({
                  title: '⚠️ 权限不足',
                  content: '需要授权保存视频到相册\n\n请按以下步骤操作：\n1. 点击"确定"打开设置\n2. 找到"保存到相册"权限\n3. 开启权限后重试',
                  showCancel: true,
                  confirmText: '去设置',
                  success: function(res) {
                    if (res.confirm) {
                      wx.openSetting({
                        success: function(settingRes) {
                          console.log('设置页面打开成功:', settingRes)
                        }
                      })
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
          console.error('下载视频失败，状态码:', downloadRes.statusCode)
        }
      },

      fail: function(err) {
        wx.hideLoading()
        console.error('下载视频失败:', err)

        let errorMsg = '下载失败'

        if (err.errMsg) {
          if (err.errMsg.includes('timeout') || err.errMsg.includes('Timeout')) {
            errorMsg = '⏰ 下载超时\n视频较大，请检查网络后重试'
          } else if (err.errMsg.includes('abort')) {
            errorMsg = '❌ 下载被中断，请重试'
          } else if (err.errMsg.includes('network')) {
            errorMsg = '🌐 网络连接失败，请检查网络'
          } else if (err.errMsg.includes('invalid')) {
            errorMsg = '🔗 视频链接已失效'
          } else {
            errorMsg = '❌ ' + err.errMsg.split(':')[0]
          }
        }

        wx.showModal({
          title: '下载失败',
          content: errorMsg + '\n\n提示：抖海视频链接有时效性，建议尽快保存',
          showCancel: true,
          confirmText: '重试',
          cancelText: '取消',
          success: function(res) {
            if (res.confirm) {
              console.log('用户点击重试')
              that.downloadVideo(videoUrl, title)
            }
          }
        })
      }
    })
  },

  downloadImage(imageUrl, title) {
    wx.showLoading({ title: '正在下载图片...', mask: true })

    const that = this
    const fileName = `${title}_${Date.now()}.jpg`

    wx.downloadFile({
      url: imageUrl,
      filePath: wx.env.USER_DATA_PATH + '/' + fileName,
      timeout: 60000, // 1分钟超时

      success: function(downloadRes) {
        wx.hideLoading()

        if (downloadRes.statusCode === 200) {
          console.log('图片下载完成，正在保存...')

          wx.saveImageToPhotosAlbum({
            filePath: downloadRes.filePath,
            success: function(saveRes) {
              wx.showToast({
                title: '图片已保存到相册',
                icon: 'success',
                duration: 2000
              })
              console.log('图片保存成功:', saveRes)
            },
            fail: function(saveErr) {
              console.error('保存图片失败:', saveErr)

              if (saveErr.errMsg && saveErr.errMsg.includes('auth deny')) {
                wx.showModal({
                  title: '⚠️ 权限不足',
                  content: '需要授权保存图片到相册\n\n请按以下步骤操作：\n1. 点击"确定"打开设置\n2. 找到"保存到相册"权限\n3. 开启权限后重试',
                  showCancel: true,
                  confirmText: '去设置',
                  success: function(res) {
                    if (res.confirm) {
                      wx.openSetting({
                        success: function(settingRes) {
                          console.log('设置页面打开成功:', settingRes)
                        }
                      })
                    }
                  }
                })
              } else {
                wx.showToast({
                  title: '保存失败: ' + (saveErr.errMsg || '未知错误'),
                  icon: 'none',
                  duration: 3000
                })
              }
            }
          })
        } else {
          wx.showToast({
            title: `下载失败: HTTP ${downloadRes.statusCode}`,
            icon: 'none',
            duration: 3000
          })
          console.error('下载图片失败，状态码:', downloadRes.statusCode)
        }
      },

      fail: function(err) {
        wx.hideLoading()
        console.error('下载图片失败:', err)

        let errorMsg = '下载失败'

        if (err.errMsg) {
          if (err.errMsg.includes('timeout') || err.errMsg.includes('Timeout')) {
            errorMsg = '下载超时，请重试'
          } else if (err.errMsg.includes('abort')) {
            errorMsg = '下载被中断，请重试'
          } else if (err.errMsg.includes('invalid')) {
            errorMsg = '图片链接已失效'
          } else {
            errorMsg = err.errMsg.split(':')[0]
          }
        }

        wx.showToast({
          title: errorMsg,
          icon: 'none',
          duration: 3000
        })
      }
    })
  },

  downloadImages(images, title) {
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

        console.log(`批量下载完成 - 成功: ${successCount}, 失败: ${failCount}`)
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
                console.log(`图片 ${index + 1} 保存成功`)
                updateProgress()
                downloadNext(index + 1)
              },
              fail: function() {
                failCount++
                console.error(`图片 ${index + 1} 保存失败`)
                updateProgress()
                downloadNext(index + 1)
              }
            })
          } else {
            failCount++
            console.error(`图片 ${index + 1} 下载失败，状态码: ${downloadRes.statusCode}`)
            updateProgress()
            downloadNext(index + 1)
          }
        },

        fail: function(err) {
          failCount++
          console.error(`图片 ${index + 1} 下载失败:`, err)
          updateProgress()
          downloadNext(index + 1)
        }
      })
    }

    downloadNext(0)
  }
})
