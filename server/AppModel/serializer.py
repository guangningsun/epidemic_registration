from rest_framework import serializers
from AppModel.models import *
from rest_framework.decorators import api_view


class AssetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AssetInfo
        fields = ('id','asset_name','asset_count','asset_type','asset_sn','asset_band','asset_specification','asset_unit','asset_image','asset_limit_nu','asset_limit_price','asset_if_deduct')

class SupplierSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SupplierAssetInfo
        fields = ('id','supplier_name','supplier_name_id','price')

class BudgetInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BudgetInfo
        fields = ('category','year','month','budget','cost_num','surplus','status')

class UserInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserInfo
        fields = ('nick_name','user_name','weixin_openid','phone_number','category','auth','address')


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserInfo
        fields = ('login_name','weixin_id','phone_number','category','address')


class CommodityCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CommodityCategory
        fields = ('id','name','parent','slug','image')


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id','name','parent','slug','surplus')

class OrderInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderInfo
        fields = ('id','order_status','order_is_special','order_create_time','order_items','order_total_price','order_image','order_apartment','order_user','order_exceed_reason')