<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="content">家庭成员</block>
		</cu-custom>
		
		<view class="cu-card" v-for="(item, index) in member_list" :key="index" @tap="goToModifyInfo(item, index)">
			<view class="cu-item" style="margin-bottom: -10upx;">
				<view class=" cu-list menu-avatar" >
					<view class="cu-item padding-left" style="height: 200upx;">
						<view class="cu-avatar lg margin-left-sm bg-white">
							<image
								:src="item.gender == undefined || item.gender == null || item.gender == '' ? '/static/defaulthead.png' : item.gender == '男' ? '/static/headm.png' : '/static/headf.png'"
								style="width: 120upx; height: 100upx;"
							></image>
						</view>
						<view class="content4" style="width: calc(100% - 220upx);">
							<view class="flex justify-between">
								<view class="title text-lg">{{item.name == undefined || item.name == null || item.name == "" ? '成员姓名' : item.name}}</view>
								<view class="xl cuIcon-write"></view>
							</view>
							<view class="text-grey ">
								{{item.gender == undefined || item.gender == null || item.gender == "" ? '基本信息（待填写）' : item.gender + ' | ' + item.age + '岁 | ' + item.tel_num}}
							</view>
							
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<view class="justify-between bottom-box">
			<view class="padding flex flex-direction">
				<button class="cu-btn bg-blue lg" :disabled="btn_disabled" @click="onSubmit">
					完成
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
			family_meneber_num : 0
		};
	},

	onLoad(option) {
		console.log(option)
		if(option.memberListInfo !== undefined){
			let info = JSON.parse(decodeURIComponent(option.memberListInfo));
			this.member_list = info;
			console.log(this.member_list);
		}
		else{
			this.member_list = getApp().globalData.member_list_info;
			if(this.member_list == undefined || this.member_list.length == 0){
				console.log("家庭成员为空，手动填写");
				this.family_meneber_num = uni.getStorageSync(getApp().globalData.key_family_num);
				for(var i = 0; i < this.family_meneber_num; i++){
					var memberInfo = {
						name:"",
						gender:"",
						age:"",
						nation:"",
						id_num:"",
						tel_num:"",
						address:uni.getStorageSync(getApp().globalData.key_address),
						work_place:"",
						
						has_disease_radio:"",
						disease_index:-1,
						disease_name:"",
						should_show_other_disease:false,
						
						medicine_name:"",
						has_take_medicine_radio:""
					}
					this.member_list.push(memberInfo);
				}
			}
			else{
				console.log("家庭成员为非空，展示已有的");
			}
		}
	},

	methods: {
		goToModifyInfo(e, index) {
			console.log(index);
			uni.navigateTo({
				url: 'suspected_family_info?member_index=' + index
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
			
			var valid = true;
			for(var i = 0; i < this.member_list.length; i++){
				var temp = this.member_list[i];
				if(this.isEmpty(temp.name)){
					valid = false;
					break;
				}
			}
			
			if(!valid){
				this.showToast("请完善家庭成员信息后再提交")
				return;
			}
			
			uni.showLoading({
				title:'正在提交...'
			})
			
			let params = {
				family_contact_name: uni.getStorageSync(getApp().globalData.key_family_contact),
				family_tel_num: uni.getStorageSync(getApp().globalData.key_tel),
				family_address: uni.getStorageSync(getApp().globalData.key_address),
				family_member_num: uni.getStorageSync(getApp().globalData.key_family_num),
				family_member_list: JSON.stringify(this.member_list)
			};
									
			this.requestWithMethod(
				getApp().globalData.api_create_family_info,
				"POST",
				params,
				this.successCallback,
				this.failCallback,
				this.completeCallback);
		},
		successCallback(rsp) {
			uni.hideLoading();
			if (rsp.data.error === 0) {
				uni.showToast({
					title:'提交成功'
				});
				uni.requestSubscribeMessage({
				  tmplIds: ['UUIzbUHXPhqQC5S3ujtGVE-5uta4PPTAilKewh9sf9o'],
				  success (res) {
					  console.log('subscribe msg: ');
					  console.log(res);
				  }
				})
				uni.navigateTo({
					url:'./family_index'
				})
			}else{
				uni.showToast({
					title:'操作失败'
				});
			}
		},
		failCallback(err) {
			uni.hideLoading();
			this.showToast(err);
			console.log('api_create_family_info failed', err);
		},
		completeCallback(rsp) {},
	}
};
</script>

<style></style>
