//index.js
//获取应用实例
const app = getApp()
Page({
  data: {
    motto: 'Hello World',
    redirect_url: '',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    console.log('onload2')
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function(e) {
    console.log('e',e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
    wx.request({
      url: 'https://pinkslash.metatype.cn/api/mini_login/',
      header: {
        'content-type': 'application/json'
      },
      data: {
        status: 'firstLogin',
        code: app.globalData.code,
        userInfo: e.detail.userInfo,
      },
      method: "POST",
      success: function (result) {
        console.log(result)
        var redirect_url = result.data.result.url
        console.log('redirect_url', redirect_url)
        app.globalData.redirect_url = redirect_url
      }
    })
  },
  goBaidu: function () {
    wx.navigateTo({
      url: '../out/out', //
      success: function () {
      },       //成功后的回调；
      fail: function () { },         //失败后的回调；
      complete: function () { }      //结束后的回调(成功，失败都会执行)
    })
  }
})
