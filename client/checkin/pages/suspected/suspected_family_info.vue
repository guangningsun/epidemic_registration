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
					
					<view class="cu-form-group" v-show="has_disease_radio === '有'">
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
					
					<view class="cu-form-group" v-show="has_take_medicine_radio === '有'">
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
			age:0,
			
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
			
		};
	},

	onLoad() {
		this.address = uni.getStorageSync(getApp().globalData.key_address);
	},

	methods: {
		RadioChange(e) {
			this.gender = e.detail.value
			console.log(this.gender)
		},
		
		HasDiseaseRadioChange(e){
			this.has_disease_radio = e.detail.value;
			console.log(this.has_disease_radio)
		},
		HasTakeMedicineRadioChange(e){
			this.has_take_medicine_radio = e.detail.value;
			console.log(this.has_take_medicine_radio)
		},
		
		DiseasePickerChange(e){
			this.disease_index = e.detail.value;
			if (this.disease_index == -1) {
			    this.disease_index = 0;
			} else {
			    this.disease_index = e.detail.value;
			}
			this.disease_name = this.disease_list[this.disease_index];

			if(this.disease_name === '其他'){
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

		},
		

		////////////////////

		checkBtnEnable() {
			console.log(this.family_num);
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
				this.isEmpty(this.has_take_medicine_radio)

			) {
				this.btn_disabled = true;
			} else {
				this.btn_disabled = false;
			}
		},
		onSubmit(){
			
			uni.setStorageSync(getApp().globalData.key_family_num,this.family_num);
			uni.setStorageSync(getApp().globalData.key_address,this.address);
			uni.setStorageSync(getApp().globalData.key_tel,this.tel_num);
			uni.setStorageSync(getApp().globalData.key_family_contact,this.family_contact);
			
			uni.navigateTo({
				url:'suspected_family_info'
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
