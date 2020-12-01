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
						
						<view class="cu-avatar lg margin-left-sm bg-white">
							<image
								:src="item.gender == undefined || item.gender == null || item.gender == '' ? '/static/defaulthead.png' : item.gender == '男' ? '/static/headm.png' : '/static/headf.png'"
								style="width: 120upx; height: 100upx;"
							></image>
						</view>
						
						<view class="content4" style="width: calc(100% - 220upx);">
							<view class="flex justify-between">
								<view class="title text-lg text-bold">{{item.name}}</view>
								<view class="cu-btn round lines-blue" @tap="onShowDetail(item)">详情</view>
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
									@input="changeRoom($event, item)"
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
		
		<!-- modal -->
		<view class="cu-modal" :class="modalName == 'DetailModal' ? 'show' : ''">
			<view class="cu-dialog" >
				<view class="cu-bar bg-white justify-end">
					<view class="content">详情</view>
					<view class="action" @tap="hideModal">
						<text class="cuIcon-close text-light-purple"></text>
					</view>
				</view>
				
				<scroll-view
					scroll-y
					scroll-with-animation

				>
					<view class="cu-form-group">
						<text class="title">姓名</text>
						<view>{{current_item_info.name}}</view>
					</view>
					
					<view class="cu-form-group">
						<view class="title">性别</view>
						<view>{{current_item_info.gender}}</view>
					</view>
					
					<view class="cu-form-group">
						<text class="title">年龄</text>
						<view>{{current_item_info.age}}</view>
					</view>
					
					<view class="cu-form-group" >
						<text class="title">民族</text>
						<view>{{current_item_info.nation}}</view>
						
					</view>
					
					<view class="cu-form-group">
						<text class="title">身份证号码</text>
						<view>{{current_item_info.id_num}}</view>
					</view>
					
					<view class="cu-form-group">
						<text class="title">联系电话</text>
						<view>{{current_item_info.tel_num}}</view>
					</view>
					
					<view class="cu-form-group">
						<text class="title">家庭地址</text>
						<view>{{current_item_info.address}}</view>
					</view>
					
					<view class="cu-form-group">
						<text class="title">工作单位</text>
						<view>{{current_item_info.work_place}}</view>
					</view>

					<view class="cu-form-group">
						<view class="title">有无病史</view>
						<view>{{current_item_info.has_disease_radio ? '有' : '无'}}</view>
					</view>
					
					<view class="cu-form-group" v-show="current_item_info.has_disease_radio">
						<text class="title">病史</text>
						<view>{{current_item_info.disease_name}}</view>
					</view>
					

					<view class="cu-form-group">
						<view class="title">有无服用药物</view>
						<view>{{current_item_info.has_take_medicine_radio ? '有' : '无'}}</view>
					</view>
					
					<view class="cu-form-group" v-show="current_item_info.has_take_medicine_radio">
						<text class="title">使用药物</text>
						<view>{{current_item_info.medicine_name}}</view>
					</view>
				</scroll-view>
		
				<view class="cu-bar bg-white justify-end">
					<view class="action">
						<button class="cu-btn line-blue" @tap="hideModal">了解</button>
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
			member_list:[],
			family_member_num : 0,
			family_info:"",
			modalName: null,
			current_item_info:""
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
		
		showModal(e) {
			this.modalName = 'DetailModal';
			this.current_item_info = e;
			console.log("-=-=-=");
			console.log(e);
		},
		
		hideModal(e) {
			this.modalName = null;
		},
		onShowDetail(item) {
			this.showModal(item);
		},

		changeRoom(event, item) {
			console.log(event);
			item.room = event.detail.value;
			console.log(item);
			// if (
			// 	this.isEmpty(this.family_contact) ||
			// 	this.family_num <= 0 ||
			// 	this.isEmpty(this.tel_num) ||
			// 	this.isEmpty(this.address)
			// ) {
			// 	this.btn_disabled = true;
			// } else {
			// 	this.btn_disabled = false;
			// }
			
			
		},
		onSubmit(){
			
			uni.showLoading({
				title: '正在分配',
			});
			
			for(var i = 0; i < this.member_list.length; i++){
				var tempMember = this.member_list[i];
				let params = {
					id_num: tempMember.id_num,
					room: tempMember.room,
					hotel: tempMember.hotel
				};
				
				this.requestWithMethod(
					getApp().globalData.api_update_family_info,
					"POST",
					params,
					this.successCallback,
					this.failCallback,
					this.completeCallback);
					
				setTimeout(function() {
					uni.navigateBack({
						delta: 1
					});
					uni.showToast({
						icon:'success',
						title:'分配成功'
					})
				}, 2000);
				
				// let promiseArr = [];
				// let p = new Promise((resolve, reject) => {
				//     //当第三方api提供的是异步方法时
				//     this.requestWithMethod(
				//     	getApp().globalData.api_update_family_info,
				//     	"POST",
				//     	params,
				//     	this.successCallback,
				//     	this.failCallback,
				//     	this.completeCallback);
				//     });
				// promiseArr.push(p)
				
				// //等所有promise任务执行完毕后再执行
				// Promise.all(promiseArr).then(res => {
				//     uni.navigateBack({
				// 		delta: 1
				// 	});
				// })
			}
		},
		successCallback(rsp) {
			uni.hideLoading();
			if (rsp.data.error === 0) {
				console.log("分配成功");
			}
		},
		failCallback(err) {
			uni.hideLoading();
			this.showToast(err);
			console.log('api_update_family_info failed', err);
		},
		completeCallback(rsp) {},
	}
};
</script>

<style></style>
