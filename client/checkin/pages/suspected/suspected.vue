<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="content">请输入家庭信息</block>
		</cu-custom>

		<view class="cu-card">
			<view class="cu-item">
				<form>
					<view class="cu-form-group">
						<text class="cuIcon-title text-red"></text>
						<text class="title">家庭联系人</text>
						<input
							placeholder="请输入家庭联系人"
							name="input"
							class="text-right"
							@input="checkBtnEnable"
							v-model="family_contact"
						/>
					</view>
					<view class="cu-form-group">
						<text class="cuIcon-title text-red"></text>
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
						<text class="cuIcon-title text-red"></text>
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
						<text class="cuIcon-title text-red"></text>
						<text class="title">同行隔离家庭人数</text>
						<picker @change="PickerChange" :value="index" :range="picker">
							<view class="picker">
								{{index>-1?picker[index]:'选择家庭成员数'}}
							</view>
						</picker>
					</view>
				</form>
			</view>

			<view class="justify-between bottom-box">
				<view class="padding flex flex-direction">
					<button class="cu-btn bg-blue lg" :disabled="btn_disabled" @click="onSubmit">
						下一步，填写家人信息
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
			family_contact: '',
			tel_num:'',
			address: '',
			
			picker: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
			index: -1,
			family_num: 0,
			btn_disabled: true,
			
			family_info:""
		};
	},

	onLoad(option) {
		this.tel_num = uni.getStorageSync(getApp().globalData.key_phone_num);
		
		console.log(option)
		if(option.familyInfo !== undefined){
			let info = JSON.parse(decodeURIComponent(option.familyInfo));
			this.family_info = info;
			console.log(this.family_info);
			
			this.family_contact = this.family_info.family_contact_name;
			this.tel_num = this.family_info.tel_num;
			this.address = this.family_info.family_address;
			this.family_num = this.family_info.family_member_num;
			
			this.index = this.picker.indexOf(this.family_num);
			
			getApp().globalData.member_list_info = this.family_info.family_member_list;
			
			this.checkBtnEnable();
		}
	},

	methods: {
		PickerChange(e) {
			this.index = e.detail.value;
			if (this.index == -1) {
			    this.index = 0;
			} else {
			    this.index = e.detail.value;
			}
			this.family_num = this.picker[this.index];
			this.checkBtnEnable();
			
		},
	

		////////////////////

		checkBtnEnable() {
			console.log(this.family_num);
			if (
				this.isEmpty(this.family_contact) ||
				this.family_num <= 0 ||
				this.isEmpty(this.tel_num) ||
				this.isEmpty(this.address)
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
				url:'./suspected_family_member_list'
			})
			
			console.log("=====");
			console.log(uni.getStorageSync(getApp().globalData.key_family_contact));
			console.log(uni.getStorageSync(getApp().globalData.key_tel));
			console.log(uni.getStorageSync(getApp().globalData.key_address));
			console.log( uni.getStorageSync(getApp().globalData.key_family_num));
			console.log("======")
			
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
