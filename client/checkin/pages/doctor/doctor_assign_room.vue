<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="content">房间分配</block>
		</cu-custom>
		
		<view class="cu-bar bg-white" style="min-height: 100upx;">
			<view class='margin-left title text-xl text-bold'>
				{{family_contact}}的家庭
			</view>
		</view>
		
		<view class="cu-card" v-for="(item, index) in member_list" :key="index">
			<view class="cu-item" >
				<view class=" cu-list menu-avatar" >
					<view class="cu-item padding-left" style="height: 220upx;">
						<view
							class="cu-avatar lg margin-left-sm bg-white"
							:style="'background-image:url(../../static/defaultHead.png);'"
						></view>
						<view class="content4" style="width: calc(100% - 220upx);">
							<view class="flex justify-between">
								<view class="title text-lg text-bold">{{item.name}}</view>
							</view>
							<view class="text-grey ">
								基本信息（待填写）
							</view>
							<view class="solid margin-top-sm">
								<input
								style="height: 60upx;"
									placeholder="请分配房间号"
									name="input"
									class="text-left"
									@input="checkBtnEnable"
									v-model="item.room"
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
			member_list:[1,2],
			family_meneber_num : 0
		};
	},

	onLoad() {
		// this.family_meneber_num = uni.getStorageSync(getApp().globalData.key_family_num);
		// for(var i = 0; i < this.family_meneber_num; i++){
		// 	var memberInfo = {
		// 		name:"",
		// 		gender:"",
		// 		age:0,
		// 		nation:"",
		// 		id_num:"",
		// 		tel_num:"",
		// 		address:uni.getStorageSync(getApp().globalData.key_address),
		// 		work_place:"",
				
		// 		has_disease_radio:"",
		// 		disease_index:-1,
		// 		disease_name:"",
		// 		should_show_other_disease:false,
				
		// 		medicine_name:"",
		// 		has_take_medicine_radio:""
		// 	}
		// 	this.member_list.push(memberInfo);
		// }
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
