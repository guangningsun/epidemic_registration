(global["webpackJsonp"]=global["webpackJsonp"]||[]).push([["pages/suspected/family_index"],{"3afb":function(t,e,n){"use strict";(function(t){Object.defineProperty(e,"__esModule",{value:!0}),e.default=void 0;var n={data:function(){return{familyInfo:"",headImg:"../../static/home.png",nickname:"--",tel_num:"--",member_list:[]}},onLoad:function(){var e=t.getStorageSync(getApp().globalData.key_phone_num);this.tel_num=e},onShow:function(){this.loadData()},methods:{onGoToFamilyModify:function(e){t.navigateTo({url:"suspected?familyInfo="+JSON.stringify(this.familyInfo)}),getApp().globalData.isModifyMember=!0},successCb:function(t){console.log(t.data),0===t.data.error&&(this.familyInfo=t.data.msg.family_info,this.member_list=this.familyInfo.family_member_list,getApp().globalData.member_list_info=this.member_list)},failCb:function(t){console.log("api_get_family_info failed",t)},completeCb:function(t){},loadData:function(){this.requestWithMethod(getApp().globalData.api_get_family_info+this.tel_num,"GET","",this.successCb,this.failCb,this.completeCb)}}};e.default=n}).call(this,n("543d")["default"])},"6def":function(t,e,n){"use strict";(function(t){n("e072");a(n("66fd"));var e=a(n("c20a"));function a(t){return t&&t.__esModule?t:{default:t}}t(e.default)}).call(this,n("543d")["createPage"])},"7c1b":function(t,e,n){"use strict";var a;n.d(e,"b",(function(){return i})),n.d(e,"c",(function(){return o})),n.d(e,"a",(function(){return a}));var i=function(){var t=this,e=t.$createElement;t._self._c},o=[]},c20a:function(t,e,n){"use strict";n.r(e);var a=n("7c1b"),i=n("ed07");for(var o in i)"default"!==o&&function(t){n.d(e,t,(function(){return i[t]}))}(o);var f,l=n("f0c5"),u=Object(l["a"])(i["default"],a["b"],a["c"],!1,null,null,null,!1,a["a"],f);e["default"]=u.exports},ed07:function(t,e,n){"use strict";n.r(e);var a=n("3afb"),i=n.n(a);for(var o in a)"default"!==o&&function(t){n.d(e,t,(function(){return a[t]}))}(o);e["default"]=i.a}},[["6def","common/runtime","common/vendor"]]]);