<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="content">房间分配</block>
		</cu-custom>
		
		<view class="cu-bar bg-white" style="min-height: 100upx;">
			<view class='margin-left title text-xl text-bold'>
				{{family_info.family_contact_name}}的家庭
			</view>
		</view>
		
		<view class="cu-card" v-for="(item, index) in member_list" :key="index">
			<view class="cu-item" >
				<view class=" cu-list menu-avatar" >
					<view class="cu-item padding-left" style="height: 220upx;">
						<view
							class="cu-avatar lg margin-left-sm bg-white"
							:style="item.gender == undefined || item.gender == null || item.gender == '' ? 'background-image:url(../../static/defaultHead.png);' : item.gender == '男' ? 'background-image:url(../../static/head-m.png);' : 'background-image:url(../../static/head-f.png);'"
						></view>
						<view class="content4" style="width: calc(100% - 220upx);">
							<view class="flex justify-between">
								<view class="title text-lg text-bold">{{item.name}}</view>
							</view>
							<view class="text-grey ">
								{{item.gender + ' | ' + item.age + '岁 | ' + item.tel_num}}
							</view>
							<view class="solid margin-top-sm">
								<input
								style="height: 60upx;"
									placeholder="请分配房间号"
									name="input"
									class="text-left"
									@input="checkBtnEnable"
									v-model="item.room == '(未分配)' || item.room == '-' ? '' : item.room"
								/>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<view class="justify-between bottom-box">
			<view class="padding flex flex-direction">
				<button class="cu-btn bg-blue lg" :disabled="btn_disabled" @click="onSubmit">
					完成分配
				</button>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			member_list:[],
			family_member_num : 0,
			family_info:"",
		};
	},

	onLoad(option) {
		if(option.familyInfo !== undefined){
			console.log(option.familyInfo);
			let info = JSON.parse(option.familyInfo);
			this.family_info = info;
			console.log('====');
			console.log(this.family_info);
			this.member_list = this.family_info.family_member_list;
			console.log('=====____')
			console.log(this.member_list);
			
			// this.family_contact = this.family_info.family_contact_name;
			// this.tel_num = this.family_info.tel_num;
			// this.address = this.family_info.family_address;
			// this.family_num = this.family_info.family_member_num;
			
			// this.index = this.picker.indexOf(this.family_num);
			
			// getApp().globalData.member_list_info = this.family_info.family_member_list;
			
			// this.checkBtnEnable();
		}
	},

	methods: {
		goToModifyInfo(e) {
			uni.navigateTo({
				url:'./suspected_family_info'
			})
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
						
			// uni.navigateTo({
			// 	url:'suspected_family_info'
			// })
			
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
