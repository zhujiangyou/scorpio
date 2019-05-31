//app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    // 登录
    wx.login({
      success: res => {
        this.globalData.code = res.code
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        var code = res.code
        wx.getUserInfo({
          success: res => {
            // 可以将 res 发送给后台解码出 unionId
            this.globalData.userInfo = res.userInfo
            // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
            // 所以此处加入 callback 以防止这种情况
            if (this.userInfoReadyCallback) {
              this.userInfoReadyCallback(res)
            }
            var self = this
            wx.request({
              url: 'https://pinkslash.metatype.cn/api/mini_login/',
              header: {
                'content-type': 'application/json'
              },
              data: {
                status:'secondLogin',
                code: code,
                userInfo: res
              },
              method: "POST",
              success: function (result) {
                var redirect_url = result.data.result.url
                console.log('redirect_url', redirect_url)
                self.globalData.redirect_url = redirect_url
              }
            })
          },
          fail:res=>{
            console.log('123',res)
          }
        })
      }
    })
    // 获取用户信息
    wx.getSetting({
      success: res => {
        console.log(res)
        if (res.authSetting['scope.userInfo']) {
          console.log('getsettings')
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo
              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      },
      fail:res=>{
        console.log('getsetting', res)
      }
    })
  },
  globalData: {
    userInfo: null,
    code:'',
    redirect_url:''
  }
})