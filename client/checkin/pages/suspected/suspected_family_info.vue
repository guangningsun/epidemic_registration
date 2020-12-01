<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="content">个人信息</block>
		</cu-custom>
		
		<view class="cu-bar bg-gradual-light-blue" style="min-height: 80upx;">
			<view class='action text-sm'>
				温馨提示：所填信息必须真实有效。
			</view>
		</view>
		
		<view class=""></view>

		<view class="cu-card">
			<view class="cu-item">
				<form>
					<view class="cu-form-group">
						<text class="title">姓名</text>
						<input
							placeholder="请输入姓名"
							name="input"
							class="text-right"
							@input="checkBtnEnable"
							v-model="name"
						/>
					</view>
					
					<radio-group class="block" @change="RadioChange">
						<view class="cu-form-group">
							<view class="title">性别</view>
							<view>
									男
								<radio class='blue radio margin-left-sm margin-right-sm' :class="gender=='男'?'checked':''" :checked="gender=='男'?true:false" value="男"></radio>
									女
								<radio class='blue radio margin-left-sm margin-right-sm' :class="gender=='女'?'checked':''" :checked="gender=='女'?true:false" value="女"></radio>
							</view>
						</view>
					</radio-group>
					
					<view class="cu-form-group">
						<text class="title">年龄</text>
						<input
							type="number"
							placeholder="请填写年龄"
							class="text-right"
							@input="checkBtnEnable"
							v-model="age"
						/>
					</view>
					
					<view class="cu-form-group" >
						<text class="title">民族</text>
						<picker @change="NationPickerChange" :value="nation_index" :range="nation_list">
							<view class="picker">
								{{nation_index>-1?nation_list[nation_index]:'选择民族'}}
							</view>
						</picker>
					</view>
					
					<view class="cu-form-group">
						<text class="title">身份证号码</text>
						<input
							placeholder="请输入身份证号码"
							name="input"
							class="text-right"
							@input="checkBtnEnable"
							v-model="id_num"
						/>
					</view>
					
					<view class="cu-form-group">
						<text class="title">联系电话</text>
						<input
							type="number"
							placeholder="请填写联系电话"
							class="text-right"
							@input="checkBtnEnable"
							v-model="tel_num"
						/>
					</view>
					
					<view class="cu-form-group">
						<text class="title">家庭地址</text>
						<input
							placeholder="请填写家庭地址"
							name="input"
							class="text-right"
							@input="checkBtnEnable"
							v-model="address"
						/>
					</view>
					
					<view class="cu-form-group">
						<text class="title">工作单位</text>
						<input
							placeholder="请填写工作单位"
							name="input"
							class="text-right"
							@input="checkBtnEnable"
							v-model="work_place"
						/>
					</view>
					
					<radio-group class="block" @change="HasDiseaseRadioChange">
						<view class="cu-form-group">
							<view class="title">有无病史</view>
							<view>
									无
								<radio class='blue radio margin-left-sm margin-right-sm' :class="has_disease_radio=='无'?'checked':''" :checked="has_disease_radio=='无'?true:false" value="无"></radio>
									有
								<radio class='blue radio margin-left-sm margin-right-sm' :class="has_disease_radio=='有'?'checked':''" :checked="has_disease_radio=='有'?true:false" value="有"></radio>
							</view>
						</view>
					</radio-group>
					
					<view class="cu-form-group" v-show="has_disease_radio == '有'">
						<text class="title">病史</text>
						<picker @change="DiseasePickerChange" :value="disease_index" :range="disease_list">
							<view class="picker">
								{{disease_index>-1?disease_list[disease_index]:'选择病史'}}
							</view>
						</picker>
					</view>
					
					<view class="cu-form-group" v-show="should_show_other_disease">
						<text class="title">其他病史</text>
						<input
							placeholder="请输入病史"
							name="input"
							class="text-right"
							@input="checkBtnEnable"
							v-model="disease_name"
						/>
					</view>
					
					<radio-group class="block" @change="HasTakeMedicineRadioChange">
						<view class="cu-form-group">
							<view class="title">有无服用药物</view>
							<view>
									无
								<radio class='blue radio margin-left-sm margin-right-sm' :class="has_take_medicine_radio=='无'?'checked':''" :checked="has_take_medicine_radio=='无'?true:false" value="无"></radio>
									有
								<radio class='blue radio margin-left-sm margin-right-sm' :class="has_take_medicine_radio=='有'?'checked':''" :checked="has_take_medicine_radio=='有'?true:false" value="有"></radio>
							</view>
						</view>
					</radio-group>
					
					<view class="cu-form-group" v-show="has_take_medicine_radio == '有'">
						<text class="title">使用药物</text>
						<input
							placeholder="请输入药物"
							name="input"
							class="text-right"
							@input="checkBtnEnable"
							v-model="medicine_name"
						/>
					</view>
				</form>
			</view>

			<view class="justify-between bottom-box">
				<view class="padding flex flex-direction">
					<button class="cu-btn bg-blue lg" :disabled="btn_disabled" @click="onSubmit">
						保存信息
					</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			name:"",
			gender:"",
			age:'',
			
			nation:"",
			nation_index:-1,
			nation_list:[
            "汉族", "壮族", "满族", "回族", "苗族", "维吾尔族", "土家族", "彝族", "蒙古族", "藏族", "布依族", "侗族", "瑶族", "朝鲜族", "白族", "哈尼族",
            "哈萨克族", "黎族", "傣族", "畲族", "傈僳族", "仡佬族", "东乡族", "高山族", "拉祜族", "水族", "佤族", "纳西族", "羌族", "土族", "仫佬族", "锡伯族",
            "柯尔克孜族", "达斡尔族", "景颇族", "毛南族", "撒拉族", "布朗族", "塔吉克族", "阿昌族", "普米族", "鄂温克族", "怒族", "京族", "基诺族", "德昂族", "保安族",
            "俄罗斯族", "裕固族", "乌孜别克族", "门巴族", "鄂伦春族", "独龙族", "塔塔尔族", "赫哲族", "珞巴族"],
			
			id_num:"",
			tel_num:"",
			address:"",
			work_place:"",
			
			has_disease_radio:"",
			disease_list:["健康", "妊娠","高血压","糖尿病","心血管疾病","脑血管疾病","精神疾患","其他"],
			disease_index:-1,
			disease_name:"",
			should_show_other_disease:false,
			
			medicine_name:"",
			has_take_medicine_radio:"",
			
			btn_disabled:true,
			
			member_index:""   ,//在member列表中的位置
			
			toastMsg:""
			
		};
	},

	onLoad(option) {
		this.address = uni.getStorageSync(getApp().globalData.key_address);
		
		console.log(option)
		if(option.member_index !== undefined){
			this.member_index = option.member_index;
			console.log("member_index:===");
			console.log(this.member_index);
			
			var target = getApp().globalData.member_list_info[this.member_index];
			console.log(target);
			if(!this.isEmpty(target.name)){
				this.name = target.name;
				this.gender = target.gender;
				this.age = target.age;
				this.nation = target.nation;
				this.id_num = target.id_num;
				this.tel_num = target.tel_num;
				this.address = target.address;
				this.work_place = target.work_place;
				this.has_disease_radio = target.has_disease_radio ? '有' : '无';
				this.disease_name = target.disease_name;
				this.has_take_medicine_radio = target.has_take_medicine_radio ? '有' : '无';
				this.medicine_name = target.medicine_name;
				
				this.nation_index = this.nation_list.indexOf(this.nation);
				this.disease_index = this.disease_list.indexOf(this.disease_name);
				
				this.checkBtnEnable();
			}
		}
	},

	methods: {
		RadioChange(e) {
			this.gender = e.detail.value
			console.log(this.gender)
			this.checkBtnEnable();
		},
		
		HasDiseaseRadioChange(e){
			this.has_disease_radio = e.detail.value;
			console.log(this.has_disease_radio)
			if(this.has_disease_radio == '无'){
				this.disease_name = "";
			}
			this.checkBtnEnable()
		},
		HasTakeMedicineRadioChange(e){
			this.has_take_medicine_radio = e.detail.value;
			console.log(this.has_take_medicine_radio)
			if(this.has_take_medicine_radio == '无'){
				this.medicine_name = "";
			}
			this.checkBtnEnable()
		},
		
		DiseasePickerChange(e){
			this.disease_index = e.detail.value;
			if (this.disease_index == -1) {
			    this.disease_index = 0;
			} else {
			    this.disease_index = e.detail.value;
			}
			this.disease_name = this.disease_list[this.disease_index];

			if(this.disease_name == '其他'){
				this.should_show_other_disease = true;
				this.disease_name = '';
			}
			else{
				this.should_show_other_disease = false;
			}

			this.checkBtnEnable();
		},
		
		NationPickerChange(e){
			this.nation_index = e.detail.value;
			if (this.nation_index == -1) {
			    this.nation_index = 0;
			} else {
			    this.nation_index = e.detail.value;
			}
			this.nation = this.nation_list[this.nation_index];
				
			console.log(this.nation);
			this.checkBtnEnable();
		},
		

		////////////////////

		checkBtnEnable() {
			// console.log(this.family_num);
			if (
				this.isEmpty(this.name) ||
				this.isEmpty(this.gender) ||
				this.age <= 0 ||
				this.isEmpty(this.nation) ||
				this.isEmpty(this.id_num) ||
				this.isEmpty(this.tel_num) ||
				this.isEmpty(this.has_disease_radio) ||
				this.isEmpty(this.address) ||
				this.isEmpty(this.work_place) ||
				this.isEmpty(this.has_take_medicine_radio) ||
				((this.has_disease_radio == '有' && this.isEmpty(this.disease_name)
					|| (this.has_take_medicine_radio == '有' && this.isEmpty(this.medicine_name)) ))
			) {
				this.btn_disabled = true;
			} else{
				this.btn_disabled = false
			}
			console.log(this.btn_disabled)
		},
		
		identityCode(code){
			var city={11:"北京",12:"天津",13:"河北",14:"山西",15:"内蒙古",21:"辽宁",22:"吉林",23:"黑龙江 ",31:"上海",32:"江苏",33:"浙江",34:"安徽",35:"福建",36:"江西",37:"山东",41:"河南",42:"湖北 ",43:"湖南",44:"广东",45:"广西",46:"海南",50:"重庆",51:"四川",52:"贵州",53:"云南",54:"西藏 ",61:"陕西",62:"甘肃",63:"青海",64:"宁夏",65:"新疆",71:"台湾",81:"香港",82:"澳门",91:"国外 "};
			var pass = true;
			var msg = "验证成功";
			//验证身份证格式（6个地区编码，8位出生日期，3位顺序号，1位校验位）
			if(!code || !/^\d{6}(18|19|20)?\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}(\d|[xX])$/.test(code)){
				pass=false;
				msg = "身份证号格式错误";
			}else if(!city[code.substr(0,2)]){
				pass=false;
				msg = "身份证号地址编码错误";
			}else{
				//18位身份证需要验证最后一位校验位
				if(code.length == 18){
					code = code.split('');
					//∑(ai×Wi)(mod 11)
					//加权因子
					var factor = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2 ];
					//校验位
					var parity = [ 1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2 ];
					var sum = 0;
					var ai = 0;
					var wi = 0;
					for (var i = 0; i < 17; i++)
					{
						ai = code[i];
						wi = factor[i];
						sum += ai * wi;
					}
					if(parity[sum % 11] != code[17].toUpperCase()){
						pass=false;
						msg = "身份证号校验位错误";
					}
				}
			}
			this.toastMsg = msg;
			return pass ;
		},
		
		onSubmit(){
			
			var isValidTel = this.isPoneAvailable(this.tel_num);
			if(!isValidTel){
				console.log('tel_num not valid!');
				this.showToast('手机号非法，请重新输入');
				return;
			}
			
			var isValidId = this.identityCode(this.id_num);
			if(!isValidId){
				console.log('id_num not valid!');
				this.showToast(this.toastMsg);
				return;
			}
			
			var member = {
				name:this.name,
				gender:this.gender,
				age:this.age,
				nation:this.nation,
				id_num:this.id_num,
				tel_num:this.tel_num,
				address:this.address,
				work_place:this.work_place,
				has_disease_radio:this.has_disease_radio == '有' ? true : false,
				disease_name:this.disease_name,
				has_take_medicine_radio:this.has_take_medicine_radio == '有' ? true : false,
				medicine_name:this.medicine_name,
			};
			
			console.log(getApp().globalData.member_list_info);
			if(getApp().globalData.member_list_info.length > this.member_index){
				getApp().globalData.member_list_info.set(this.member_index, member)
			}
			
			console.log(getApp().globalData.member_list_info);
			
			uni.navigateTo({
				url:'suspected_family_member_list'
			})
			
			// let params = {
			// 	openid: uni.getStorageSync(getApp().globalData.key_wx_openid),
			// 	nickname: this.nickname,
			// 	username: this.user_name,
			// 	address: this.address,
			// 	apartment: apart_id
			// };
			
			// this.requestWithMethod(
			// 	getApp().globalData.api_submit_user_info,
			// 	"POST",
			// 	params,
			// 	this.successCallback,
			// 	this.failCallback,
			// 	this.completeCallback);
		},
		// successCallback(rsp) {
		// 	uni.hideLoading();
		// 	if (rsp.data.error === 0) {
		// 		uni.setStorageSync(getApp().globalData.key_cat,this.commoditycategory);
		// 		uni.showToast({
		// 			title:'提交成功'
		// 		});
		// 		uni.navigateTo({
		// 			url:'../category/category'
		// 		})
		// 	}
		// },
		// failCallback(err) {
		// 	uni.hideLoading();
		// 	this.showToast(err);
		// 	console.log('api_submit_user_info failed', err);
		// },
		// completeCallback(rsp) {},
	}
};
</script>

<style></style>
