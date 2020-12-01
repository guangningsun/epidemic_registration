<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="false">
			<block slot="content">分配列表</block>
		</cu-custom>

		<scroll-view scroll-x class="bg-white nav text-center">
			<view class="cu-item" :class="index==TabCur?'text-blue cur':''" v-for="(item,index) in tabTitle" :key="index" @tap="tabSelect" :data-id="index">
				{{tabTitle[index]}}({{index == 0 ? allNum : notYetNum}})
			</view>
		</scroll-view>
		
		<view class="cu-bar bg-white search" >
			<view class="search-form round">
				<text class="cuIcon-search"></text>
				<input type="text" placeholder="输入搜索的关键词" confirm-type="search" v-model="search_word"></input>
			</view>
			<view class="action">
				<button class="cu-btn bg-gradual-blue shadow-blur round" @tap="onSearch">搜索</button>
			</view>
		</view>
		
		<view v-show="TabCur == 0" class="cu-card card-margin" style="margin-bottom: -30upx;" v-for="(item,index) in family_list" :key="index" @tap="goToAssignRoom(item,index)">
			<view class="cu-item">
				<view class="flex justify-between">
					<view class="flex align-center text-left margin-top-sm margin-left-sm text-gray" style="width: 100%;">{{item.registerTime}}</view>
					<view class="cu-tag radius bg-green">{{item.checkin_status}}</view>
				</view>
				<view class="flex align-center">
					<view>
						<image class="margin-left-sm" :src="'../../static/home.png'" style="width: 100upx; height: 100upx;"></image>
						<view class="padding-bottom-sm padding-left-sm justify-center text-bold text-dark-blue">家庭号:<br>{{item.family_id}}</view>
					</view>
					
					<view class="margin-left-sm">
						<view class="text-bold">{{item.family_contact_name}}的家庭</view>
						<view>家庭人数: {{item.family_member_num}}</view>
						<view>家庭住址: {{item.family_address}}</view>
					</view>
				</view>
			</view>
		</view>
		
		<view v-show="TabCur == 1" class="cu-card card-margin" style="margin-bottom: -30upx;" v-for="(item,index) in family_not_yet_list" :key="index" @tap="goToAssignRoom(item,index)">
			<view class="cu-item">
				<view class="flex justify-between">
					<view class="flex align-center text-left margin-top-sm margin-left-sm text-gray" style="width: 100%;">{{item.registerTime}}</view>
					<view class="cu-tag radius bg-green">{{item.checkin_status}}</view>
				</view>
				<view class="flex">
					<image class="margin" :src="'../../static/home.png'" style="width: 100upx; height: 100upx;"></image>
					<view class="margin-top-sm">
						<view class="text-bold">{{item.family_contact_name}}的家庭</view>
						<view>家庭人数: {{item.family_member_num}}</view>
						<view>家庭住址: {{item.family_address}}</view>
					</view>
				</view>
			</view>
		</view>
		
	</view>
</template>

<script>
export default {
	data() {
		return {
			
			TabCur: 0,
			scrollLeft: 0,
			tabTitle:['全部家庭','待分配'],
			
			allNum:0,
			notYetNum:0,
			
			family_list:[],
			search_word:'',
			
			family_not_yet_list:[]
		};
	},

	onLoad() {

	},
	
	onShow() {
		this.requestAllFamilyInfo();
	},

	methods: {
		tabSelect(e) {
			this.TabCur = e.currentTarget.dataset.id;
			console.log(this.TabCur);
			this.requestAllFamilyInfo();
		},
		
		goToAssignRoom(e, index){
			
			uni.navigateTo({
				url: 'doctor_assign_room?familyInfo=' + JSON.stringify(e)
			})
		},
		
		onSearch(){
			this.requestWithMethod(
				getApp().globalData.api_fuzzy_query + this.search_word,
				'GET',
				'',
				this.successCb,
				this.failCb,
				this.completeCb
			);
		},
		
		requestAllFamilyInfo() {
			this.requestWithMethod(
				getApp().globalData.api_get_all_family_info,
				'GET',
				'',
				this.successCb,
				this.failCb,
				this.completeCb
			);
		},
		successCb(rsp) {
			if (rsp.data.error === 0) {
				this.family_list = rsp.data.msg;
				console.log(this.family_list);
				this.allNum = this.family_list.length;
				
				this.family_not_yet_list = [];
				for(var i = 0; i < this.allNum; i ++){
					var temp = this.family_list[i];
					if(temp.checkin_status == '未分配'){
						this.family_not_yet_list.push(temp);
					}
				}
				
				this.notYetNum = this.family_not_yet_list.length;

				// var apartments = this.apartment_picker;
				// this.apartment_info_list.map(function(item) {
				// 	apartments.push(item.name);
				// });
				// console.log("==apart==");
				// console.log(apartments);
			}
		},
		failCb(err) {
			console.log('api_get_all_family_info/api_fuzzy_query failed', err);
		},
		completeCb(rsp) {},

		// ////////////////////

		// apartPickerChange(e) {
		// 	this.apartment_picker_index = parseInt(e.detail.value);
		// 	if (this.apartment_picker_index === -1) {
		// 		this.apartment_picker_index = 0;
		// 	} else {
		// 		this.apartment_picker_index = parseInt(e.detail.value);
		// 	}
		// 	this.checkBtnEnable();
			
		// },
		// checkBtnEnable() {
		// 	if (
		// 		this.date == '' ||
		// 		this.apartment_picker[this.apartment_picker_index] == '' ||
		// 		this.apartment_picker[this.apartment_picker_index] == undefined ||
		// 		this.isEmpty(this.tel_num) ||
		// 		this.isEmpty(this.user_name)
		// 	) {
		// 		this.btn_disabled = true;
		// 	} else {
		// 		this.btn_disabled = false;
		// 	}
		// },
		// onSubmit(){
		// 	if (this.apartment_picker[this.apartment_picker_index] !== undefined) {
		// 	    this.apartment = this.apartment_picker[this.apartment_picker_index];
		// 	}
			
		// 	uni.showLoading({
		// 		title: '正在提交信息',
		// 	})
			
		// 	let info = this.apartment_info_list[this.apartment_picker_index];
		// 	let apart_id = info.id;
		// 	this.apartment_id = apart_id;
			
		// 	uni.setStorageSync(getApp().globalData.key_user_name,this.user_name);
			
		// 	let params = {
		// 		openid: uni.getStorageSync(getApp().globalData.key_wx_openid),
		// 		nickname: this.nickname,
		// 		username: this.user_name,
		// 		address: this.address,
		// 		apartment: apart_id
		// 	};
			
		// 	this.requestWithMethod(
		// 		getApp().globalData.api_submit_user_info,
		// 		"POST",
		// 		params,
		// 		this.successCallback,
		// 		this.failCallback,
		// 		this.completeCallback);
		// },
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
