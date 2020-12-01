<template>
	<view class="main_body">
		<cu-custom bgColor="bg-gradual-blue" :isBack="false">
			<block slot="content">防疫登记平台</block>
		</cu-custom>

		<view v-show="!shouldShowContent && showCenterIcon">
			<view class="justify-center l-center">
				<image
					src="../../static/home_index.png"
					style="width: 330upx; height: 330upx;"
				></image>
				<button
					class="bg-light-blue margin-bottom-sm text-df margin-top-xl"
					open-type="getPhoneNumber"
					lang="zh_CN"
					@getphonenumber="getPhoneNumber"
				>
					手机号登录
				</button>
			</view>

			<view
				class="text-gray text-center justify-center padding-sm"
				style="position:fixed; bottom:0;"
			>
				{{ hint }}
			</view>

		</view>

<!-- 		<view v-show="shouldShowContent">
			<view
				class="cu-list grid col-1 no-border"
				style="margin-top: 70upx; padding-top: 40upx;"
			>
				<view class="cu-item" @tap="onClickScan">
					<view class="flex justify-center">
						<image
							src="../../static/scan.png"
							style="width: 80upx; height: 80upx;"
						></image>
					</view>
					<text class="margin-top-sm">扫码领用</text>
				</view>

			</view>
		</view> -->

		<!-- 申请手机号modal -->
		<view class="cu-modal bottom-modal" :class="modalName == 'PhoneModal' ? 'show' : ''">
			<view class="cu-dialog">
				<view class="cu-bar bg-white justify-end">
					<view class="content">手机号登录</view>
					<view class="action" @tap="hideModal">
						<text class="cuIcon-close text-light-purple"></text>
					</view>
				</view>
				<view class="padding-xl">{{ hint }}</view>
				<view class="cu-bar bg-white">
					<view class="flex justify-end action">
						<button class="cu-btn text-gray" @tap="hideModal">拒绝</button>
						<button
							class="cu-btn line-olive margin-left-sm"
							open-type="getPhoneNumber"
							lang="zh_CN"
							@getphonenumber="getPhoneNumber"
						>
							同意
						</button>
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
			modalName: null,

			openid: '',
			headImg: '../../static/submit1.png',
			user_nickname: '',
			user_phone: '',
			user_auth: '',
			user_info:null,
			
			apartmentId:'',

			shouldShowContent: false,
			showCenterIcon: true,

			hint:
				'登录后可以完整使用防疫登记服务。首次使用，需要授权获取您的手机号进行登录绑定。'
		};
	},
	onLoad: function(options) {
		// console.log('======二维码解析参数========');
		// console.log(options.q);
		// var scene = decodeURIComponent(options.q); // 使用decodeURIComponent解析  获取当前二维码的网址
		// var arr1 = scene.split('/');
		// var apartId = arr1[arr1.length - 1];
		// this.apartmentId = apartId;
		// console.log(this.apartmentId);
		// uni.setStorageSync(getApp().globalData.key_cat, this.apartmentId);
	},
	onShow() {
		this.user_phone = uni.getStorageSync(getApp().globalData.key_phone_num);
		this.openid = uni.getStorageSync(getApp().globalData.key_wx_openid);
		this.user_auth = uni.getStorageSync(getApp().globalData.key_user_auth);

		uni.login({
			provider: 'weixin',
			success: loginRes => {
				console.log('+++code：' + loginRes.code);

				this.requestWithMethod(
					getApp().globalData.api_login + loginRes.code,
					'POST',
					'',
					this.successCb,
					this.failCb,
					this.completeCb
				);
			}
		});
	},
	methods: {
		showPhoneModal(e) {
			this.modalName = e;
		},
		hideModal(e) {
			this.modalName = null;
		},

		successCb(rsp) {
			console.log('weixin_sns success');
			console.log(rsp);
			if (rsp.data.error === 0) {
				this.openid = rsp.data.openid;
				let is_login = rsp.data.is_login;
				let user_auth = rsp.data.auth;

				// console.log(this.openid);
				
				uni.setStorageSync(getApp().globalData.key_user_auth,user_auth);

				uni.setStorageSync(getApp().globalData.key_wx_openid,rsp.data.openid);

				////////
				console.log('is_login:' + is_login);
				if (is_login == 0) {
					this.showPhoneModal('PhoneModal');
				} else {
					console.log('auth:' + user_auth);
					uni.showLoading({
						title: '登录中.......'
					});
					this.requestUserInfo();
				}
			}
		},
		failCb(err) {
			console.log('api_login failed', err);
		},
		completeCb(rsp) {},
/////
		successGetUserInfoCb(rsp) {
			uni.hideLoading();
			if (rsp.data.error === 0) {
				this.user_info = rsp.data.msg.user_info;
				console.log(this.user_info);
				
				// let user_name = this.user_info[0].user_name;
				// console.log('user_name====' + user_name);
				// uni.setStorageSync(getApp().globalData.key_user_name, user_name);
				// if(this.isEmpty(user_name)){
				// 	uni.navigateTo({
				// 		url:'./user_info'
				// 	});
				// }else{
					let user_auth = uni.getStorageSync(getApp().globalData.key_user_auth)
					if (user_auth == 0) {
						uni.setStorageSync(getApp().globalData.key_user_name,this.user_info[0].user_name);
						uni.setStorageSync(getApp().globalData.key_phone_num,this.user_info[0].phone_number);

						uni.hideLoading();
						uni.navigateTo({
							url:'../suspected/suspected'
						})
					} else if (user_auth == 1) {
						uni.hideLoading();
						uni.navigateTo({
							url: '../doctor/doctor_family_list'
						});
					} else {
						this.showToast('未知错误!');
					}
				// }
			}
		},
		failGetUserInfoCb(err) {
			uni.hideLoading();
			console.log('get_user_info failed', err);
		},
		completeGetUserInfoCb(rsp) {},
		
		requestUserInfo() {
			let param
			this.requestWithMethod(
				getApp().globalData.get_user_info + this.openid,
				'GET',
				'',
				this.successGetUserInfoCb,
				this.failGetUserInfoCb,
				this.completeGetUserInfoCb
			);
		},

		onGotUserInfo(e) {
			console.log(e);
			console.log(e.detail.userInfo.avatarUrl);
			this.user_nickname = e.detail.userInfo.nickName;
			uni.setStorageSync( getApp().globalData.key_user_head, e.detail.userInfo.avatarUrl);
			uni.setStorageSync(getApp().globalData.key_user_nickname, e.detail.userInfo.nickName);
		},

		///////////////

		// 0: 普通用户， 1:管理
		successPhoneCb(rsp) {
			console.log('api_phone success, rsp======');
			console.log(rsp);
			this.showCenterIcon = false;

			if (this.containsStr(rsp.errMsg, 'ok')) {
				uni.setStorageSync(getApp().globalData.key_phone_num,rsp.data.purePhoneNumber);
				uni.setStorageSync(getApp().globalData.key_user_auth,rsp.data.auth);

				let auth = rsp.data.auth;
				console.log('phone cb auth: ' + auth);
				uni.hideLoading();
				this.requestUserInfo();
				// if (auth === '0') {
				// 	//如果是微信扫一扫过来的，拿到了部门id之后，直接跳转到分类页
				// 	if(!this.isEmpty(this.apartmentId)){
				// 		uni.hideLoading();
				// 		uni.navigateTo({
				// 			url:'../category/category'
				// 		})
				// 	}else{
				// 		this.shouldShowContent = true;
				// 	}
				// } else if (auth === '1' || auth === '2' || auth === '3') {
				// 	uni.navigateTo({
				// 		url: '../approve/approve'
				// 	});
				// }
			}
		},
		failPhoneCb(err) {
			console.log('api_phone failed', err);
		},
		completePhoneCb(rsp) {},

		getPhoneNumber(e) {
			this.hideModal();

			var that = this;
			// 拒绝授权
			if (e.detail.errMsg == 'getPhoneNumber:fail user deny') {
				uni.showModal({
					title: '提示',
					showCancel: false,
					content: '未授权将无法登录',
					success: function(res) {}
				});
			} else {
				uni.showLoading({
					title: '跳转中'
				});

				let params = {
					encryptedData: e.detail.encryptedData,
					iv: e.detail.iv,
					openid: this.openid
				};
				this.requestWithMethod(
					getApp().globalData.api_getWXInfo,
					'POST',
					params,
					this.successPhoneCb,
					this.failPhoneCb,
					this.completePhoneCb
				);
			}
		}
	}
};
</script>

<style>
.l-center {
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
}
page {
background-color: #fcfff5;
}
</style>
