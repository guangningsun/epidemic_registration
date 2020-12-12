(global["webpackJsonp"]=global["webpackJsonp"]||[]).push([["pages/suspected/suspected_family_info"],{"093e":function(e,i,s){"use strict";var t;s.d(i,"b",(function(){return a})),s.d(i,"c",(function(){return n})),s.d(i,"a",(function(){return t}));var a=function(){var e=this,i=e.$createElement;e._self._c},n=[]},2474:function(e,i,s){"use strict";(function(e){Object.defineProperty(i,"__esModule",{value:!0}),i.default=void 0;var s={data:function(){return{name:"",gender:"",age:"",nation:"",nation_index:-1,nation_list:["汉族","壮族","满族","回族","苗族","维吾尔族","土家族","彝族","蒙古族","藏族","布依族","侗族","瑶族","朝鲜族","白族","哈尼族","哈萨克族","黎族","傣族","畲族","傈僳族","仡佬族","东乡族","高山族","拉祜族","水族","佤族","纳西族","羌族","土族","仫佬族","锡伯族","柯尔克孜族","达斡尔族","景颇族","毛南族","撒拉族","布朗族","塔吉克族","阿昌族","普米族","鄂温克族","怒族","京族","基诺族","德昂族","保安族","俄罗斯族","裕固族","乌孜别克族","门巴族","鄂伦春族","独龙族","塔塔尔族","赫哲族","珞巴族"],id_num:"",tel_num:"",address:"",work_place:"",has_disease_radio:"",disease_list:["健康","妊娠","高血压","糖尿病","心血管疾病","脑血管疾病","精神疾患","其他"],disease_index:-1,disease_name:"",should_show_other_disease:!1,medicine_name:"",has_take_medicine_radio:"",btn_disabled:!0,member_index:"",toastMsg:""}},onLoad:function(i){if(this.address=e.getStorageSync(getApp().globalData.key_address),console.log(i),void 0!==i.member_index){this.member_index=i.member_index,console.log("member_index:==="),console.log(this.member_index);var s=getApp().globalData.member_list_info[this.member_index];console.log(s),this.isEmpty(s.name)||(this.name=s.name,this.gender=s.gender,this.age=s.age,this.nation=s.nation,this.id_num=s.id_num,this.tel_num=s.tel_num,this.address=s.address,this.work_place=s.work_place,this.has_disease_radio=s.has_disease_radio?"有":"无",this.disease_name=s.disease_name,this.has_take_medicine_radio=s.has_take_medicine_radio?"有":"无",this.medicine_name=s.medicine_name,this.nation_index=this.nation_list.indexOf(this.nation),this.disease_index=this.disease_list.indexOf(this.disease_name),this.checkBtnEnable())}},methods:{RadioChange:function(e){this.gender=e.detail.value,console.log(this.gender),this.checkBtnEnable()},HasDiseaseRadioChange:function(e){this.has_disease_radio=e.detail.value,console.log(this.has_disease_radio),"无"==this.has_disease_radio&&(this.disease_name=""),this.checkBtnEnable()},HasTakeMedicineRadioChange:function(e){this.has_take_medicine_radio=e.detail.value,console.log(this.has_take_medicine_radio),"无"==this.has_take_medicine_radio&&(this.medicine_name=""),this.checkBtnEnable()},DiseasePickerChange:function(e){this.disease_index=e.detail.value,-1==this.disease_index?this.disease_index=0:this.disease_index=e.detail.value,this.disease_name=this.disease_list[this.disease_index],"其他"==this.disease_name?(this.should_show_other_disease=!0,this.disease_name=""):this.should_show_other_disease=!1,this.checkBtnEnable()},NationPickerChange:function(e){this.nation_index=e.detail.value,-1==this.nation_index?this.nation_index=0:this.nation_index=e.detail.value,this.nation=this.nation_list[this.nation_index],console.log(this.nation),this.checkBtnEnable()},checkBtnEnable:function(){this.isEmpty(this.name)||this.isEmpty(this.gender)||this.age<=0||this.isEmpty(this.nation)||this.isEmpty(this.id_num)||this.isEmpty(this.tel_num)||this.isEmpty(this.has_disease_radio)||this.isEmpty(this.address)||this.isEmpty(this.work_place)||this.isEmpty(this.has_take_medicine_radio)||"有"==this.has_disease_radio&&this.isEmpty(this.disease_name)||"有"==this.has_take_medicine_radio&&this.isEmpty(this.medicine_name)?this.btn_disabled=!0:this.btn_disabled=!1,console.log(this.btn_disabled)},identityCode:function(e){var i={11:"北京",12:"天津",13:"河北",14:"山西",15:"内蒙古",21:"辽宁",22:"吉林",23:"黑龙江 ",31:"上海",32:"江苏",33:"浙江",34:"安徽",35:"福建",36:"江西",37:"山东",41:"河南",42:"湖北 ",43:"湖南",44:"广东",45:"广西",46:"海南",50:"重庆",51:"四川",52:"贵州",53:"云南",54:"西藏 ",61:"陕西",62:"甘肃",63:"青海",64:"宁夏",65:"新疆",71:"台湾",81:"香港",82:"澳门",91:"国外 "},s=!0,t="验证成功";if(e&&/^\d{6}(18|19|20)?\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}(\d|[xX])$/.test(e))if(i[e.substr(0,2)]){if(18==e.length){e=e.split("");for(var a=[7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2],n=[1,0,"X",9,8,7,6,5,4,3,2],d=0,o=0,h=0,_=0;_<17;_++)o=e[_],h=a[_],d+=o*h;n[d%11]!=e[17].toUpperCase()&&(s=!1,t="身份证号校验位错误")}}else s=!1,t="身份证号地址编码错误";else s=!1,t="身份证号格式错误";return this.toastMsg=t,s},onSubmit:function(){var i=this.isPoneAvailable(this.tel_num);if(!i)return console.log("tel_num not valid!"),void this.showToast("手机号非法，请重新输入");var s=this.identityCode(this.id_num);if(!s)return console.log("id_num not valid!"),void this.showToast(this.toastMsg);var t={name:this.name,gender:this.gender,age:this.age,nation:this.nation,id_num:this.id_num,tel_num:this.tel_num,address:this.address,work_place:this.work_place,has_disease_radio:"有"==this.has_disease_radio,disease_name:this.disease_name,has_take_medicine_radio:"有"==this.has_take_medicine_radio,medicine_name:this.medicine_name};console.log(getApp().globalData.member_list_info),getApp().globalData.member_list_info.length>this.member_index&&getApp().globalData.member_list_info.set(this.member_index,t),console.log(getApp().globalData.member_list_info),e.navigateBack({delta:1})}}};i.default=s}).call(this,s("543d")["default"])},"47c5":function(e,i,s){"use strict";s.r(i);var t=s("093e"),a=s("b2bf");for(var n in a)"default"!==n&&function(e){s.d(i,e,(function(){return a[e]}))}(n);var d,o=s("f0c5"),h=Object(o["a"])(a["default"],t["b"],t["c"],!1,null,null,null,!1,t["a"],d);i["default"]=h.exports},5564:function(e,i,s){"use strict";(function(e){s("e072");t(s("66fd"));var i=t(s("47c5"));function t(e){return e&&e.__esModule?e:{default:e}}e(i.default)}).call(this,s("543d")["createPage"])},b2bf:function(e,i,s){"use strict";s.r(i);var t=s("2474"),a=s.n(t);for(var n in t)"default"!==n&&function(e){s.d(i,e,(function(){return t[e]}))}(n);i["default"]=a.a}},[["5564","common/runtime","common/vendor"]]]);