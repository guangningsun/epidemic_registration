# -*- coding:UTF-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.admin import DraggableMPTTAdmin
from feincms.module.page.models import Page
import datetime
from django.utils.html import format_html
from AppModel import *


class UserInfo(models.Model):
    AUTH_CHOICES = [
    ('0', '员工'),
    ('1', '主管'),
    ('2', '主任'),
    ('3', '管理员'),
    ]
    nick_name = models.CharField(max_length=200,verbose_name='微信名')
    user_name = models.CharField(max_length=200,verbose_name='用户名')
    weixin_openid = models.CharField(max_length=200,verbose_name='微信ID')
    phone_number = models.CharField(max_length=200,verbose_name='手机号')
    category = TreeForeignKey('Category',on_delete=models.CASCADE,null=True,blank=True,verbose_name='所属部门')
    auth = models.CharField(max_length=200, choices=AUTH_CHOICES,verbose_name='用户权限')
    address = models.CharField(max_length=200,verbose_name='常用地址')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
    
    def __str__(self):
        return self.user_name


class AssetInfo(models.Model):
    asset_name = models.CharField(max_length=200,verbose_name='物品名称')
    asset_sn = models.CharField(max_length=200,verbose_name='物品编码')
    asset_type = models.CharField(max_length=200,verbose_name='物品型号')
    asset_count = models.CharField(max_length=200,verbose_name='物品库存')
    asset_band = models.CharField(max_length=200,verbose_name='物品品牌')
    asset_specification = models.CharField(max_length=200,verbose_name='物品规格')
    asset_band = models.CharField(max_length=200,verbose_name='物品品牌')
    asset_unit = models.CharField(max_length=200,verbose_name='计量单位')
    asset_image = models.ImageField(u'物品图片',null=True, blank=True, upload_to='asset_image')
    asset_ccategory = models.ForeignKey('CommodityCategory',on_delete=models.CASCADE,null=True,blank=True,verbose_name='类别标签')
    asset_limit_nu = models.CharField(max_length=200,verbose_name='申领数量限制')
    asset_limit_price = models.CharField(max_length=200,verbose_name='申领单价限制')
    asset_if_deduct = models.BooleanField(verbose_name='是否抵扣部门余额',default="False") 
    # asset_supplier = models.ForeignKey('SupplierInfo',on_delete=models.CASCADE,null=True,blank=True,verbose_name='供应商')
    # asset_price = models.CharField(max_length=200,verbose_name='报价')

    class Meta:
        verbose_name = '物品信息'
        verbose_name_plural = '物品信息'
    
    def __str__(self):
          return (("%s %s") % (self.asset_name,self.asset_type))
    

# 组织机构详细信息
class Post(models.Model):
      name = models.CharField(max_length=120,verbose_name='单位名称')
      category = TreeForeignKey('Category',on_delete=models.CASCADE,null=True,blank=True,verbose_name='上级部门')
      createtime = models.CharField(max_length=200,verbose_name='创建时间')
      createuser = models.CharField(max_length=200,verbose_name='创建者')
      connected_number = models.CharField(max_length=200,verbose_name='联系电话')
      slug = models.SlugField(verbose_name='标签')
      
      def __str__(self):
          return self.name

#物品分类
class CommodityCategory(MPTTModel):
      name = models.CharField(max_length=50, unique=True,verbose_name='名称')
      parent = TreeForeignKey('self' ,null=True, blank=True,on_delete=models.CASCADE, related_name='children', db_index=True,verbose_name='上级分类')
      slug = models.SlugField(verbose_name='标签')
      image = models.ImageField(u'物品图片',null=True, blank=True, upload_to='asset_image')
    
      class MPTTMeta:
        order_insertion_by = ['name']
    
      class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'categories'
        verbose_name = '物品分类'
    
      def get_slug_list(self):
        try:
          ancestors = self.get_ancestors(include_self=True)
        except:
          ancestors = []
        else:
          ancestors = [ i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
          slugs.append('/'.join(ancestors[:i+1]))
        return slugs
    
      def __str__(self):
        return self.name



# 组织机构
class Category(MPTTModel):
      name = models.CharField(max_length=50, unique=True,verbose_name='名称')
      parent = TreeForeignKey('self', null=True, blank=True,on_delete=models.CASCADE, related_name='children', db_index=True,verbose_name='上级部门')
      slug = models.SlugField(verbose_name='标签')
      surplus = models.CharField(max_length=200, verbose_name='余额')

    
      class MPTTMeta:
        order_insertion_by = ['name']
    
      class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'categories'
        verbose_name = '组织机构'
    
      def get_slug_list(self):
        try:
          ancestors = self.get_ancestors(include_self=True)
        except:
          ancestors = []
        else:
          ancestors = [ i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
          slugs.append('/'.join(ancestors[:i+1]))
        return slugs
    
      def __str__(self):
        return self.name


class WeixinSessionKey(models.Model):
    weixin_openid = models.CharField(max_length=200,verbose_name='openid')
    weixin_sessionkey = models.CharField(max_length=200,verbose_name='sessionkey')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
        verbose_name = '微信用户SK'
        verbose_name_plural = '微信用户SK'

# 统计查询
class StatisticsInfo(models.Model):
  asset_name = models.CharField(max_length=120,verbose_name='物品名称')
  category_name = models.CharField(max_length=120,verbose_name='部门名称')
  claim_count = models.CharField(max_length=120,verbose_name='领用数量')


# 供应商
class SupplierInfo(models.Model):
  supplier_name = models.CharField(max_length=120,verbose_name='供应商名称')
  supplier_short = models.CharField(max_length=120,verbose_name='供应商简称')
  if_deactivate = models.BooleanField(verbose_name='是否停用',default="False") 

  class Meta:
        verbose_name = '供应商信息'
        verbose_name_plural = '供应商信息'
  
  def __str__(self):
        return self.supplier_name


# 商品
class CommodityInfo(models.Model):
      ITEM_STATUS_CHOICES = [
      ('0', '备货中'),
      ('1', '已派送'),
      ('2', '已签收'),
      ('3', '待审批通过'),
      ]
      commodity_name = models.CharField(max_length=200,verbose_name='商品名称',default="商品名称")
      commodity_unit = models.CharField(max_length=200, verbose_name='商品单位',default="商品单位")
      commodity_image = models.ImageField(u'商品图片',null=True, blank=True, upload_to='commodity_image')
      commodity_total_price = models.CharField(max_length=200, verbose_name='商品总价',default="商品总价")
      commodity_specification = models.CharField(max_length=200, verbose_name='商品规格',default="商品规格")
      commodity_create_time = models.CharField(max_length=200, verbose_name='创建时间',default="-")
      commodity_price = models.CharField(max_length=200, verbose_name='商品单价',default="商品单价")
      commodity_count = models.CharField(max_length=200, verbose_name='商品数量',default="商品数量")
      commodity_supplier = models.ForeignKey('SupplierInfo',on_delete=models.CASCADE,null=True,blank=True,verbose_name='所属供应商')
      commodity_status = models.CharField(max_length=200, choices=ITEM_STATUS_CHOICES ,verbose_name='商品状态')
      sys_username = models.CharField(max_length=200, verbose_name='系统用户名',default="系统用户名")
      commodity_username = models.CharField(max_length=200, verbose_name='订单用户',default="订单用户")
      commodity_apartment = models.CharField(max_length=200, verbose_name='订单部门',default="订单部门")
      commodity_phonenum = models.CharField(max_length=200, verbose_name='用户电话',default="用户电话")
      commodity_address = models.CharField(max_length=200, verbose_name='用户地址',default="用户地址")
      commodity_if_deduct = models.BooleanField(verbose_name='是否抵扣部门余额',default="False") 
    
      class Meta:
          verbose_name = '商品信息'
          verbose_name_plural = '商品信息'
    
      def __str__(self):
          return self.commodity_name

# 订单表
class OrderInfo(models.Model):
      ORDER_STATUS_CHOICES = [
      ('0', '待审批'),
      ('1', '审批通过'),
      ('2', '未通过'),
      ('3', '自动过单'),
      ]
      order_status = models.CharField(max_length=200, choices=ORDER_STATUS_CHOICES,verbose_name='订单状态')
      order_is_special = models.BooleanField(verbose_name='是否专项',default="False")
      order_create_time = models.CharField(max_length=200, verbose_name='创建时间',default="创建时间")
      order_items = models.ManyToManyField(CommodityInfo)
      order_total_price = models.CharField(max_length=200, verbose_name='商品总价',default="商品总价")
      order_image = models.ImageField(u'订单图片',null=True, blank=True, upload_to='order_image')
      order_apartment = models.ForeignKey('Category',on_delete=models.CASCADE,null=True,blank=True,verbose_name='所属部门')
      order_exceed_reason = models.CharField(max_length=200, verbose_name='超限原因描述',default="超限原因描述")
      order_user = models.ForeignKey('UserInfo',on_delete=models.CASCADE,null=True,blank=True,verbose_name='提交用户')

      class Meta:
          verbose_name = '订单信息'
          verbose_name_plural = '订单信息'

# 订单对应商品列表类
class MappingCommodityToOrder(models.Model):
    commodityinfo = models.ForeignKey(CommodityInfo, models.DO_NOTHING,verbose_name='商品清单')
    orderinfo = models.ForeignKey(OrderInfo, models.DO_NOTHING,verbose_name='订单')

    class Meta:
        managed = False
        db_table = 'AppModel_orderinfo_order_items'
        unique_together = (('commodityinfo', 'orderinfo'),)

# 供应商库存表
class SupplierAssetInfo(models.Model):
    supplier_name = models.ForeignKey('SupplierInfo',on_delete=models.CASCADE,null=True,blank=True,verbose_name='供应商名称')
    price = models.CharField(max_length=200, verbose_name='商品价格',default="商品价格")
    assetinfo = models.ForeignKey('AssetInfo',on_delete=models.CASCADE,null=True,blank=True,verbose_name='对应商品')
    asset_num = models.CharField(max_length=200, verbose_name='商品库存',default="商品库存")
    if_off_shelf = models.BooleanField(verbose_name='是否下架',default="False") 
    sys_username = models.CharField(max_length=200, verbose_name='系统用户名',default="系统用户名")

    class Meta:
          verbose_name = '供应商库存管理'
          verbose_name_plural = '供应商库存管理'


# 部门预算表
class BudgetInfo(models.Model):
    STATUS_CHOICES = [
      ('1', '1'),
      ('2', '2'),
      ('3', '3'),
      ('4', '4'),
      ('5', '5'),
      ('6', '6'),
      ('7', '7'),
      ('8', '8'),
      ('9', '9'),
      ('10', '10'),
      ('11', '11'),
      ('12', '12'),
      ]
    BUDGET_CHOICES = [
      ('0', '未执行'),
      ('1', '已执行'),
      ('2', '执行中'),
      ]
    category = models.ForeignKey('Category',on_delete=models.CASCADE,null=True,blank=True,verbose_name='部门')
    year = models.CharField(max_length=200, verbose_name='年度',default="年度")
    month = models.CharField(max_length=200, choices=STATUS_CHOICES,verbose_name='月度')
    budget = models.CharField(max_length=200,verbose_name='预算')
    cost_num = models.CharField(max_length=200,verbose_name='花销')
    surplus = models.CharField(max_length=200, verbose_name='余额')
    status = models.CharField(max_length=200, choices=BUDGET_CHOICES,verbose_name='执行状态')

    class Meta:
          verbose_name = '部门预算'
          verbose_name_plural = '部门预算'

