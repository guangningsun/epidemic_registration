<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="false">
			<block slot="content">我的家庭信息</block>
		</cu-custom>

		<view class="cu-card">
			<view class="flex align-center cu-item bg-gradual-light-blue padding-sm">
				<view class="flex justify-between">
					<view class="flex align-center text-left margin-top-sm margin-left-xl text-gray" style="width: 100%;"></view>
					<view class="cu-tag radius bg-olive">{{familyInfo.checkin_status}}</view>
				</view>
				
				<view class="flex  p-xs margin-bottom-sm mb-sm">
					<view class="flex-sub">
						<view class="flex align-center justify-center margin-top">
							<image
								:src="headImg"
								style="width: 160upx; height: 160upx;"
							></image>
						</view>
					</view>
					<view class="flex-twice">
						<view class=" flex text-dark-gray text-lg margin-left-sm margin-top-xl">
							<view>
								<view class="text-bold margin-bottom-xs">{{familyInfo.family_contact_name}}的家庭</view>
								<view>家庭号：{{familyInfo.family_id}}</view>
								<view>{{familyInfo.family_address}}</view>
							</view>
						</view>
					</view>
				</view>
				
				<view class="flex justify-end padding-sm margin-xs radius">
					<button
						class="cu-btn cuIcon-writefill shadow bg-cyan margin-right-xs margin-bottom-sx"
						@tap="onGoToFamilyModify"
					>
						更新家庭信息
					</button>
				</view>
			</view>
		</view>
		
		<view class=" text-gray flex justify-center">
			-------- 成员分配情况 --------
		</view>
		
		<view class="cu-card" v-for="(item, index) in member_list" :key="index" @tap="goToModifyInfo(item)">
			<view class="cu-item">
				<view class=" cu-list menu-avatar" >
					<view class="cu-item padding-left" style="height: 200upx;">
						<view class="content5" style="width: calc(100% - 100upx);">
							<view class="flex justify-between">
								<view class="title text-lg">{{item.name}}</view>
								<view class="text-bold text-dark-blue margin-top">房间号：{{item.room}}</view>
							</view>
							<view class="text-grey ">
								电话：{{item.tel_num}}
							</view>
							
						</view>
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
			
			familyInfo:'',
			
			headImg: '../../static/home.png',
			nickname:'--',
			tel_num:'--',
			
			member_list:[]

		};
	},

	onLoad() {
		// let nickname = uni.getStorageSync('key_user_nickname');
		let tel = uni.getStorageSync(getApp().globalData.key_tel);
		this.tel_num = tel;
		
	},

	onShow() {
		this.loadData();
	},

	methods: {		
		
		onGoToFamilyModify(e){
			
			// uni.navigateTo({
			// 	url: 'suspected_family_member_list?memberListInfo=' + encodeURIComponent(JSON.stringify(this.member_list))
			// })
			
			uni.navigateTo({
				url: 'suspected?familyInfo=' + JSON.stringify(this.familyInfo)
			})

		},
		
		successCb(rsp) {
			console.log(rsp.data);

			if (rsp.data.error === 0) {
				this.familyInfo = rsp.data.msg.family_info;
				this.member_list = this.familyInfo.family_member_list;
			}
		},
		failCb(err) {
			console.log('api_get_family_info failed', err);
		},
		completeCb(rsp) {},
		
		loadData() {
			
			this.requestWithMethod(
				getApp().globalData.api_get_family_info + this.tel_num,
				'GET',
				'',
				this.successCb,
				this.failCb,
				this.completeCb
			);
		},
	}
};
</script>

<style></style>
