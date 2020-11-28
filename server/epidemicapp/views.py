# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework import viewsets, filters,permissions
from AppModel.serializer import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from collections import OrderedDict
from AppModel.models import *
from django.db.models import Avg, Count, Min, Sum
import hashlib,urllib,random,logging,requests,base64
import json,time,django_filters,xlrd,uuid
from rest_framework import status
import time, datetime
import requests,configparser
from AppModel.WXBizDataCrypt import WXBizDataCrypt 
from django.conf import settings


logger = logging.getLogger(__name__)
logger.setLevel(level = logging.DEBUG)
handler = logging.FileHandler("epidemicapp.log")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


conf_dir = settings.CONF_DIR
cf = configparser.ConfigParser()
cf.read(conf_dir)
logger.info("成功加载配置文件 %s " % (conf_dir))

# 内部方法用于返回json消息
# done
def _generate_json_message(flag, message):
    if flag:
        return HttpResponse("{\"error\":0,\"msg\":\""+message+"\"}",
                            content_type='application/json',
                            )
    else:
        return HttpResponse("{\"error\":1,\"msg\":\""+message+"\"}",
                            content_type='application/json',
                            )
                            

# 获取资产列表
@api_view(['GET'])
def asset_detail(request):
    if request.method == 'GET':
        assetset = AssetInfo.objects.all()
        serializer = AssetSerializer(assetset, many=True)
        res_json = {"error": 0,"msg": {
                    "asset_info": serializer.data }}
        return Response(res_json)


# 通过物品分类 category id获取商品列表
@api_view(['GET'])
def asset_by_cid(request,cid):
    if request.method == 'GET':
        assetset = AssetInfo.objects.filter(asset_ccategory=cid)
        serializer = AssetSerializer(assetset, many=True)
        res_json = {"error": 0,"msg": {
                    "asset_info": serializer.data }}
        return Response(res_json)

# 通过物品分类 category id获取商品列表
@api_view(['GET'])
def asset_by_cname(request,cname):
    if request.method == 'GET':
        try:
            assetset = AssetInfo.objects.filter(asset_name__contains=cname)
            serializer = AssetSerializer(assetset, many=True)
            res_json = {"error": 0,"msg": {
                        "asset_info": serializer.data }}
            return Response(res_json)
        except:
            res_json = {"error": 1,"msg": {"没有该商品"}}
            return Response(res_json)


# 获取部门列表
@api_view(['GET'])
def get_category(request):
    if request.method == 'GET':
        assetset = Category.objects.all()
        serializer = CategorySerializer(assetset, many=True)
        res_json = {"error": 0,"msg": {
                    "category_info": serializer.data }}
        return Response(res_json)


# 物品申领功能
@api_view(['POST'])
def claim_asset(request):
    if request.method == 'POST':
        # claim_username = request.POST['claim_username']
        # import pdb;pdb.set_trace()
        claim_list = request.POST['choose_list']
        category = request.POST['category']
        reason = request.POST['reason']
        claim_weixin_openid = request.POST['claim_weixin_openid']
        # if_need_explanation = False
        try:
            cr = ClaimRecord(category=Category.objects.get(id=category))
            cr.save()
            for claim_submmit in json.loads(claim_list):
                claim_count = claim_submmit['claim_count']
                claim_name = claim_submmit['claim_name']
                claim_unit = claim_submmit['claim_unit']
                assetinfo = AssetInfo.objects.get(asset_name=claim_name)
                # 查看申领物品剩余是否足量
                if int(assetinfo.asset_count)<int(claim_count):
                    return _generate_json_message(False,""+claim_name+"库存商品不足")
                # 如果申请数量大于该物品限制则超限标准设置为true，转交主管审批
                if int(claim_count) > int(assetinfo.asset_limit_nu):
                    cr.if_exceed_standard = True
                    logger.info("申请商品 %s 数量  %s 大于限制数量 %s 将是否超限设置为 %s" % (claim_name,claim_count,assetinfo.asset_limit_nu, cr.if_exceed_standard))
                #     if_need_explanation = True
                #     return _generate_json_message(False,"抱歉,该部门没有权限申请过多商品")
                assetinfo.asset_count = int(assetinfo.asset_count) - int(claim_count)
                # 资产管理减少指定数量物品
                assetinfo.save()
                # 创建申领物品
                cs = Claimlist(claim_count=claim_count,claim_name=claim_name,claim_unit=claim_unit)
                cs.save()
                # 申领物品加入该条申领记录中
                cr.claim_list.add(cs)
            # 修改申领记录的所属部门和申领状态参数
            cr.category=Category.objects.get(id=category)
            cr.desc = reason
            cr.claim_weixin_openid = claim_weixin_openid
            # 通知申领结果
            ret = __weixin_send_message(claim_weixin_openid,str(cr.claim_date),"物品申领","待审批")
            # 通知审批人结果
            #ret1 = __weixin_send_message(openid, str(clr.claim_date),"物品申领","您有一条待审批通知")
            # if if_need_explanation:
            #     cr.approval_status = '1'
            # else:

            # 如果申领物品超限则给主管审批，如果未超限则直接给管理员审批
            if cr.if_exceed_standard == 'True':
                cr.approval_status = '0'
                zhuguanlist = UserInfo.objects.filter(auth='1').filter(category=category)
                for zhuguan in zhuguanlist:
                    ret1 = __weixin_send_message(zhuguan.weixin_openid, str(cr.claim_date),"物品申领","您有一条待审批通知")
            else:
                cr.approval_status = '2'
                userinfoset = UserInfo.objects.filter(auth='3')
                for userinfo in userinfoset:
                    ret1 = __weixin_send_message(userinfo.weixin_openid, str(cr.claim_date),"物品申领","您有一条待审批通知")
            cr.save()
            return _generate_json_message(True, "申领成功")
        except :
            return _generate_json_message(False, "仓库中没有该类型商品")


# 完善用户信息
@api_view([ 'POST'])
def submit_user_info(request):
    if request.method == 'POST':
        openid = request.POST['openid']
        nickname = request.POST['nickname']
        username = request.POST['username']
        apartment = request.POST['apartment']
        address = request.POST['address']
        try:
            userinfo = UserInfo.objects.get(weixin_openid=openid)
            userinfo.nick_name=nickname
            userinfo.user_name=username
            userinfo.category=Category.objects.get(id=apartment)
            userinfo.address=address
            userinfo.save()
            res_json = {"error": 0,"msg": {"更新用户信息成功"}}
            return Response(res_json)
        except:
            res_json = {"error": 0,"msg": {"更新用户信息失败"}}
            return Response(res_json)

        

# 通过微信id获取用户信息
@api_view(['GET'])
def get_user_info_by_wxid(request,weixin_id):
    if request.method == 'GET':
        userset = UserInfo.objects.filter(weixin_openid=weixin_id)
        serializer = UserInfoSerializer(userset, many=True)
        res_json = {"error": 0,"msg": {
                    "user_info": serializer.data }}
        return Response(res_json)



# 用户注册功能
@api_view(['GET', 'POST'])
def userinfo_detail(request):
    if request.method == 'GET':
        userset = UserInfo.objects.all()
        serializer = UserSerializer(userset, many=True)
        res_json = {"error": 0,"msg": {
                    "user_info": serializer.data }}
        return Response(res_json)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res_json = {"error": 0,"msg": {
                    "user_info": serializer.data }}
            return Response(res_json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 个人申领历史记录
@api_view(['GET', 'POST'])
def claim_detail(request):
    if request.method == 'GET':
        # claimset = ClaimRecord.objects.filter(claim_weixin_id=sn)
        claimset = ClaimRecord.objects.all()
        serializer = ClaimSerializer(claimset, many=True)
        res_json = {"error": 0,"msg": {
                    "claim_record_info": serializer.data }}
        return Response(res_json)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def __restore_quantity(claim_name, claim_count):
    assetinfo = AssetInfo.objects.get(asset_name=claim_name)
    assetinfo.asset_count = int(assetinfo.asset_count) + int(claim_count)
    assetinfo.save()
    logger.info("恢复申请商品 %s  的数量 %s " % (claim_name , claim_count))
    return 0



# 修改申请状态
@api_view(['POST'])
def change_approval_status(request):
    if request.method == 'POST':
        openid = request.POST['openid']
        is_rej = request.POST['is_rejectted']
        is_rejectted = True if is_rej.lower() == 'true' else False
        is_fin = request.POST['is_finished']
        is_finished = True if is_fin.lower() == 'true' else False
        reason = request.POST['reason']
        record_id = request.POST['record_id']
        #通过openid获取该用户所在部门category和权限auth
        try:
            userinfo = UserInfo.objects.get(weixin_openid=openid)
            #如果是该部门主管则将状态修改到待管理员审批
            if userinfo.auth == "1" and is_rejectted:
                # 主管未通过审批则将状态更改为 5拒绝申请
                clr = ClaimRecord.objects.get(id=record_id)
                clr.approval_status="5"
                clr.desc=reason
                clr.save()
                mc_list = MappingClaimLisToRecord.objects.filter(claimrecord=clr)
                for mc in mc_list:
                    claimlist_obj = Claimlist.objects.get(id=mc.claimlist_id)
                    cl_obj = Claimlist.objects.get(id=claimlist_obj.id)
                    __restore_quantity(cl_obj.claim_name,cl_obj.claim_count)
                logger.info("用户权限为 %s  进行了rejectted操作  %s 审批状态更改为 %s" % (userinfo.auth , is_rejectted,clr.approval_status))
                # 通知申领结果
                ret = __weixin_send_message(clr.claim_weixin_openid,str(clr.claim_date),"物品申领","主管未通过")
                # 通知审批人结果
                ret1 = __weixin_send_message(openid,str(clr.claim_date),"审批通知","您有一条待审批通知")
            elif userinfo.auth == "2" and not is_rejectted:
                # 主任通过审批则将状态更改为 2待管理员审批
                clr = ClaimRecord.objects.get(id=record_id)
                clr.approval_status="2"
                clr.save()
                mc_list = MappingClaimLisToRecord.objects.filter(claimrecord=clr)
                for mc in mc_list:
                    claimlist_obj = Claimlist.objects.get(id=mc.claimlist_id)
                    cl_obj = Claimlist.objects.get(id=claimlist_obj.id)
                    __restore_quantity(cl_obj.claim_name,cl_obj.claim_count)
                # 通知申领人
                logger.info("用户权限为 %s  进行了rejectted操作  %s 审批状态更改为 %s" % (userinfo.auth , is_rejectted,clr.approval_status))
                ret = __weixin_send_message(clr.claim_weixin_openid,str(clr.claim_date),"物品申领","已通过主任审批")
                # 通知审批人结果
                ret1 = __weixin_send_message(openid,str(clr.claim_date),"审批通知","您有一条待审批通知")
            if userinfo.auth == "2" and is_rejectted:
                # 主任未通过审批则将状态更改为 5拒绝申请
                clr = ClaimRecord.objects.get(id=record_id)
                clr.approval_status="5"
                clr.desc=reason
                clr.save()
                mc_list = MappingClaimLisToRecord.objects.filter(claimrecord=clr)
                for mc in mc_list:
                    claimlist_obj = Claimlist.objects.get(id=mc.claimlist_id)
                    cl_obj = Claimlist.objects.get(id=claimlist_obj.id)
                    __restore_quantity(cl_obj.claim_name,cl_obj.claim_count)
                # 通知申领结果
                logger.info("用户权限为 %s  进行了rejectted操作  %s 审批状态更改为 %s" % (userinfo.auth , is_rejectted,clr.approval_status))
                ret = __weixin_send_message(clr.claim_weixin_openid,str(clr.claim_date),"物品申领","主任未通过审批")
                # 通知审批人结果
                ret1 = __weixin_send_message(openid,str(clr.claim_date),"审批通知","您有一条待审批通知")
            elif userinfo.auth == "1" and not is_rejectted:
                # 主管通过审批则将状态更改为 2待管理员审批
                clr = ClaimRecord.objects.get(id=record_id)
                #如果申领物品在限额以外
                if clr.if_exceed_standard:
                    clr.approval_status="1"
                else:
                    #if 在范围内
                    clr.approval_status="2"
                clr.save()
                logger.info("用户权限为 %s  进行了rejectted操作  %s 审批状态更改为 %s 是否超限额 %s " % (userinfo.auth , is_rejectted,clr.approval_status,clr.if_exceed_standard))
                ret = __weixin_send_message(clr.claim_weixin_openid,str(clr.claim_date),"物品申领","已通过主管审批待管理员审批")
                # 通知审批人结果
                ret1 = __weixin_send_message(openid,str(clr.claim_date),"审批通知","您有一条待审批通知")
            elif userinfo.auth == "3" and not is_rejectted:
                # 管理员通过审批则将状态改为 3 审批完成待发放
                clr = ClaimRecord.objects.get(id=record_id)
                clr.approval_status="3"
                clr.save()
                # 通知申领结果
                logger.info("用户权限为 %s  进行了rejectted操作  %s 审批状态更改为 %s" % (userinfo.auth , is_rejectted,clr.approval_status))
                ret = __weixin_send_message(clr.claim_weixin_openid,str(clr.claim_date),"物品申领","已通过管理员审批待领取")
                # 通知审批人结果
                ret1 = __weixin_send_message(openid,str(clr.claim_date),"审批通知","您有一条待审批通知")
            elif userinfo.auth == "3" and is_rejectted:
                # 管理员未通过审批则将状态改为 5拒绝申请
                clr = ClaimRecord.objects.get(id=record_id)
                clr.approval_status="5"
                clr.desc=reason
                clr.save()
                # 通知申领结果
                mc_list = MappingClaimLisToRecord.objects.filter(claimrecord=clr)
                for mc in mc_list:
                    claimlist_obj = Claimlist.objects.get(id=mc.claimlist_id)
                    cl_obj = Claimlist.objects.get(id=claimlist_obj.id)
                    __restore_quantity(cl_obj.claim_name,cl_obj.claim_count)
                logger.info("用户权限为 %s  进行了rejectted操作  %s 审批状态更改为 %s" % (userinfo.auth , is_rejectted,clr.approval_status))
                ret = __weixin_send_message(clr.claim_weixin_openid,str(clr.claim_date),"物品申领","管理员未通过审批")
                # 通知审批人结果
                ret1 = __weixin_send_message(openid,str(clr.claim_date),"审批通知","您有一条待审批通知")
            if userinfo.auth == "3" and is_finished:
                clr = ClaimRecord.objects.get(id=record_id)
                clr.approval_status="4"
                clr.desc=reason
                clr.save()
                # 通知申领结果
                logger.info("用户权限为 %s  进行了rejectted操作  %s 审批状态更改为 %s" % (userinfo.auth , is_rejectted,clr.approval_status))
                ret = __weixin_send_message(clr.claim_weixin_openid,str(clr.claim_date),"物品申领","已成功领取")
                # 通知审批人结果
                ret1 = __weixin_send_message(openid,str(clr.claim_date),"审批通知","您有一条待审批通知")
            res_json = {"error": 0,"msg": "status success changed"}
            return Response(res_json)
        except:
            pass




# 获取审批列表
@api_view(['POST'])
def get_approval_list(request):
    if request.method == 'POST':
        openid = request.POST['openid']
        auth = request.POST['auth']
        
        # 待主管审批
        if auth == "1":
        # 查询管理员所在部门
            cid = UserInfo.objects.get(weixin_openid=openid).category
            claimset = ClaimRecord.objects.filter(approval_status=0).filter(category=cid)
            serializer = ClaimSerializer(claimset, many=True)
            for i in range (0,len(serializer.data)):
                for k,v in serializer.data[i].items():
                    if k == "claim_list":
                        cl =[]
                        for cli in v:
                            cl_obj = Claimlist.objects.get(id=cli)
                            col_data = cl_obj.claim_count+cl_obj.claim_unit
                            dic = {}
                            dic[Claimlist.objects.get(id=cli).claim_name]=col_data
                            cl.append(dic)
                        serializer.data[i]['claim_list'] = cl
                    if k == "category":
                        serializer.data[i]['category'] = Category.objects.get(id=v).name
                    if k == "approval_status":
                        if v == "0":
                            serializer.data[i]['approval_status'] = "待主管审批"
                        elif v == "1":
                            serializer.data[i]['approval_status'] = "待主任审批"
                        elif v == "2":
                            serializer.data[i]['approval_status'] = "待管理员审批"
                        elif v == "3":
                            serializer.data[i]['approval_status'] = "审批完成"
                        elif v == "4":
                            serializer.data[i]['approval_status'] = "已发放"
                        elif v == "5":
                            serializer.data[i]['approval_status'] = "未批准"

            res_json = {"error": 0,"msg": {
                        "approval_list_info": serializer.data }}
            return Response(res_json)
        # 待主任审批
        elif auth == "2":
            # claimset = ClaimRecord.objects.filter(approval_status=1)
            # serializer = ClaimSerializer(claimset, many=True)
            # res_json = {"error": 0,"msg": {
            #             "approval_list_info": serializer.data }}
            # return Response(res_json)
            cid = UserInfo.objects.get(weixin_openid=openid).category
            #claimset = ClaimRecord.objects.filter(approval_status=1).filter(category=cid)
            claimset = ClaimRecord.objects.filter(approval_status=1)
            serializer = ClaimSerializer(claimset, many=True)
            for i in range (0,len(serializer.data)):
                for k,v in serializer.data[i].items():
                    if k == "claim_list":
                        cl =[]
                        for cli in v:
                            cl_obj = Claimlist.objects.get(id=cli)
                            col_data = cl_obj.claim_count+cl_obj.claim_unit
                            dic = {}
                            dic[Claimlist.objects.get(id=cli).claim_name]=col_data
                            cl.append(dic)
                        serializer.data[i]['claim_list'] = cl
                    if k == "category":
                        serializer.data[i]['category'] = Category.objects.get(id=v).name
                    if k == "approval_status":
                        if v == "0":
                            serializer.data[i]['approval_status'] = "待主管审批"
                        elif v == "1":
                            serializer.data[i]['approval_status'] = "待主任审批"
                        elif v == "2":
                            serializer.data[i]['approval_status'] = "待管理员审批"
                        elif v == "3":
                            serializer.data[i]['approval_status'] = "审批完成"
                        elif v == "4":
                            serializer.data[i]['approval_status'] = "已发放"
                        elif v == "5":
                            serializer.data[i]['approval_status'] = "未批准"

            res_json = {"error": 0,"msg": {
                        "approval_list_info": serializer.data }}
            return Response(res_json)
        # 待管理员审理
        elif auth == "3":
            # claimset = ClaimRecord.objects.filter(approval_status=2)
            # serializer = ClaimSerializer(claimset, many=True)
            # res_json = {"error": 0,"msg": {
            #             "approval_list_info": serializer.data }}
            # return Response(res_json)
            cid = UserInfo.objects.get(weixin_openid=openid).category
            #claimset = ClaimRecord.objects.filter(approval_status=2).filter(category=cid)
            claimset = ClaimRecord.objects.filter(approval_status=2)
            serializer = ClaimSerializer(claimset, many=True)
            for i in range (0,len(serializer.data)):
                for k,v in serializer.data[i].items():
                    if k == "claim_list":
                        cl =[]
                        for cli in v:
                            cl_obj = Claimlist.objects.get(id=cli)
                            col_data = cl_obj.claim_count+cl_obj.claim_unit
                            dic = {}
                            dic[Claimlist.objects.get(id=cli).claim_name]=col_data
                            cl.append(dic)
                        serializer.data[i]['claim_list'] = cl
                    if k == "category":
                        serializer.data[i]['category'] = Category.objects.get(id=v).name
                    if k == "approval_status":
                        if v == "0":
                            serializer.data[i]['approval_status'] = "待主管审批"
                        elif v == "1":
                            serializer.data[i]['approval_status'] = "待主任审批"
                        elif v == "2":
                            serializer.data[i]['approval_status'] = "待管理员审批"
                        elif v == "3":
                            serializer.data[i]['approval_status'] = "审批完成"
                        elif v == "4":
                            serializer.data[i]['approval_status'] = "已发放"
                        elif v == "5":
                            serializer.data[i]['approval_status'] = "未批准"

            res_json = {"error": 0,"msg": {
                        "approval_list_info": serializer.data }}
            return Response(res_json)


# 物品分类管理
@api_view(['GET'])
def commoditycategory_detail(request):
    if request.method == 'GET':
        commoditycategoryset = CommodityCategory.objects.all()
        serializer = CommodityCategorySerializer(commoditycategoryset, many=True)
        for i in range(0,len(serializer.data)):
            assetset = AssetInfo.objects.filter(asset_ccategory=serializer.data[i]['id'])
            asset_serializer = AssetSerializer(assetset, many=True)
            serializer.data[i]["asset_info"]= asset_serializer.data
            if serializer.data[i]['parent'] == None:
                serializer.data[i]['parent'] = '-'
            if serializer.data[i]['image'] == None:
                serializer.data[i]['image'] = '-'
        res_json = {"error": 0,"msg": {
                    "commoditycategory": serializer.data }}
        return Response(res_json)



# 提交订单
@api_view(['POST'])
def submit_order(request):
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        order_apartment = request.POST['order_apartment']
        order_exceed_reason = request.POST['order_exceed_reason']
        order_is_special = request.POST['order_is_special']
        order_image = request.FILES.get('order_image',None)
        order_item_list = request.POST['order_item_list']
        order_total_price = request.POST['order_total_price']
        is_exceed = request.POST['is_exceed']
        weixin_openid = request.POST['weixin_openid']
        try:
            #判断是否超限，如果超限订单待审批order_status='0' commodity_status=3
            #如果未超限订单直接审批通过order_status='3',commodity_status=0
            msg = {"提交订单成功"}
            error = 0
            if is_exceed == "True":
                os='0'
                cs='3'
            else:
                os='3'
                cs='0'
            userinfo = UserInfo.objects.get(weixin_openid=weixin_openid)
            order_info = OrderInfo(order_apartment=Category.objects.get(id=order_apartment),
                                    order_status=os,
                                    order_is_special=order_is_special,
                                    order_create_time=int(time.time()),
                                    order_total_price=order_total_price,
                                    order_image=order_image,
                                    order_exceed_reason=order_exceed_reason,
                                    order_user= userinfo
                                    )
            order_info.order_image = order_image
            order_info.save()
            # 部门花销增加，余额减少
            current_month = datetime.datetime.now().month
            try:
                budgetinfo = BudgetInfo.objects.get(category=Category.objects.get(id=order_apartment),month=current_month)
                current_cost = budgetinfo.cost_num
                commodity_cost_num = 0
                deduct_cost_num = 0
                for order_item in json.loads(order_item_list):
                    asset_sn = order_item['item_sn']
                    supplier_id = order_item['item_supplier_id']
                    commodity_num = order_item['item_num']
                    commodity_total_price = order_item['item_price']
                    asset_info = AssetInfo.objects.get(asset_sn=asset_sn)
                    supplierassetinfo_list = SupplierAssetInfo.objects.filter(supplier_name=supplier_id)
                    commodity_info = CommodityInfo(commodity_name=asset_info.asset_name ,
                                                    commodity_unit=asset_info.asset_unit ,
                                                    commodity_image=asset_info.asset_image ,
                                                    #commodity_total_price=float(supplierassetinfo_list[0].price)*int(commodity_num),
                                                    commodity_total_price=commodity_total_price,
                                                    commodity_create_time=order_info.order_create_time,
                                                    commodity_specification=asset_info.asset_specification,
                                                    #commodity_price=supplierassetinfo_list[0].price,
                                                    commodity_price=float(commodity_total_price)/int(commodity_num),
                                                    commodity_count=commodity_num,
                                                    commodity_supplier=SupplierInfo.objects.get(id=supplier_id),
                                                    commodity_status=cs,
                                                    sys_username=supplierassetinfo_list[0].sys_username,
                                                    commodity_username=userinfo.user_name,
                                                    commodity_apartment=Category.objects.get(id=userinfo.category_id),
                                                    commodity_phonenum=userinfo.phone_number,
                                                    commodity_address=userinfo.address,
                                                    commodity_if_deduct=asset_info.asset_if_deduct
                                                    )
                    commodity_info.save()
                    order_info.order_items.add(commodity_info)
                    order_info.save()
                    # 如果该物品要抵扣部门余额则增加部门余额消费
                    if asset_info.asset_if_deduct == True and order_info.order_is_special == 'False':
                        #deduct_cost_num = deduct_cost_num + float(supplierassetinfo_list[0].price)*int(commodity_num)
                        deduct_cost_num = deduct_cost_num + float(commodity_total_price)
                    commodity_cost_num = commodity_cost_num + float(commodity_total_price)
                budgetinfo.surplus = float(budgetinfo.surplus) - deduct_cost_num
                budgetinfo.cost_num = float('%.2f' %(float(budgetinfo.cost_num) + commodity_cost_num))
                budgetinfo.save()
            except:
                error=1
                msg={"该部门 "+current_month+"月份未做预算"}
            res_json = {"error": error ,"msg": msg }
            return Response(res_json)
        except:
            res_json = {"error": 0,"msg": {"提交订单失败"}}
            return Response(res_json)



# 获取部门余额
@api_view(['GET'])
def get_category_surplus(request,cid):
    if request.method == 'GET':
        category = Category.objects.get(id=cid)
        current_month = datetime.datetime.now().month
        budgetinfo = BudgetInfo.objects.filter(category=category).filter(month=current_month)
        serializer = BudgetInfoSerializer(budgetinfo, many=True)
        for i in range(0,len(serializer.data)):
            serializer.data[i]["category_name"]= category.name
        res_json = {"error": 0,"msg": {
                    "budget_info": serializer.data }}
        return Response(res_json)


# 获取供应商列表
@api_view(['GET'])
def get_supplier(request,sn):
    if request.method == 'GET':
        assetinfo = AssetInfo.objects.get(asset_sn=sn)
        supplierset = SupplierAssetInfo.objects.filter(assetinfo = assetinfo.id).order_by('price').filter(if_off_shelf=False)
        serializer = SupplierSerializer(supplierset, many=True)
        res_json={}
        for i in range (0,len(serializer.data)):
            sup_name=""
            try:
                for k,v in serializer.data[i].items():
                    if k == "supplier_name":
                        supplier_obj = SupplierInfo.objects.get(id=v)
                        sup_name = supplier_obj.supplier_name
                serializer.data[i]['supplier_name']=sup_name
                serializer.data[i]['asset_unit']=assetinfo.asset_unit
                res_json = {"error": 0,"msg": {
                        "supplier_list": serializer.data }}
            except:
                res_json = {"error": 1,"msg": "暂无供应商" }
        return Response(res_json)


# 获取历史订单列表
@api_view(['GET'])
def get_all_order_info_list(request,weixin_id):
    # 通过微信id拿到用户id
    userinfo = UserInfo.objects.get(weixin_openid=weixin_id)
    order_user_id = userinfo.id
    # orderinfo = OrderInfo.objects.filter(order_user_id=order_user_id)
    # 通过用户id拿到订单id list
    orderinfo_list = OrderInfo.objects.filter(order_user_id=order_user_id).order_by("-order_create_time")
    serializer = OrderInfoSerializer(orderinfo_list, many=True)
    for i in range (0,len(serializer.data)):
        for k,v in serializer.data[i].items():
            if k=="order_items":
                relist = []
                for commodity_id in v:
                    item = {}
                    commodityinfo = CommodityInfo.objects.get(id=commodity_id) 
                    item["commodity_name"] = commodityinfo.commodity_name
                    item["commodity_unit"] = commodityinfo.commodity_unit
                    item["commodity_image"] = commodityinfo.commodity_image.name
                    item["commodity_total_price"] = commodityinfo.commodity_total_price
                    item["commodity_specification"] = commodityinfo.commodity_specification
                    item["commodity_price"] = commodityinfo.commodity_price
                    item["commodity_count"] = commodityinfo.commodity_count
                    item["commodity_supplier"] = commodityinfo.commodity_supplier.supplier_name
                    cstatus ="-"
                    if commodityinfo.commodity_status == "0":
                        cstatus = "备货中"
                    elif commodityinfo.commodity_status == "1":
                        cstatus = "已派送"
                    elif commodityinfo.commodity_status == "2":
                        cstatus = "已签收"
                    elif commodityinfo.commodity_status == "3":
                        cstatus = "待审批通过"
                    item["commodity_status"] = cstatus
                    item["sys_username"] = commodityinfo.sys_username
                    relist.append(item)
                serializer.data[i]['order_items'] = relist
            if k=="order_apartment":
                serializer.data[i]['order_apartment'] = Category.objects.get(id=v).name
            if k=="order_user":
                serializer.data[i]['order_user'] = UserInfo.objects.get(id=v).user_name
            if k=="order_status":
                order_status = "-"
                if v=="0":
                    order_status="待审批"
                elif v=="1":
                    order_status="审批通过"
                elif v=="2":
                    order_status="未通过"
                elif v=="3":
                    order_status="自动过单"
                serializer.data[i]['order_status'] = order_status

    res_json = {"error": 0,"msg": {
                "order_info_list": serializer.data }}
    return Response(res_json)


# weixin 登录
@api_view(['POST'])
def weixin_sns(request,js_code):
    if request.method == 'POST':
        APPID = cf.get("WEIXIN", "weixin_appid")
        SECRET = cf.get("WEIXIN", "weixin_secret")
        JSCODE = js_code
        logger.debug("获取appid %s  secret %s" % (APPID,SECRET))
        requst_data = "https://api.weixin.qq.com/sns/jscode2session?appid="+APPID+"&secret="+SECRET+"&js_code="+JSCODE+"&grant_type=authorization_code"
        req = requests.get(requst_data)
        logger.debug("拼接的微信登录url 为 %s" % (requst_data ))
        if req.status_code == 200:
            openid = json.loads(req.content)['openid']
            session_key = json.loads(req.content)['session_key']
            # WeixinSessionKey.objects.update_or_create(weixin_openid=openid,
            #                                         weixin_sessionkey=session_key)
            is_login = "1"
            user_auth = "0"
            try:
                wsk = WeixinSessionKey.objects.get(weixin_openid=openid)
                wsk.weixin_sessionkey = session_key
                wsk.save()
                userinfo = UserInfo.objects.get(weixin_openid=openid)
                # 增加用户是否已登录
                is_login = "1"
                user_auth = userinfo.auth
            except WeixinSessionKey.DoesNotExist:
                cwsk = WeixinSessionKey(weixin_openid=openid,weixin_sessionkey=session_key)
                cwsk.save()
                is_login = "0"

            return HttpResponse("{\"error\":0,\"msg\":\"登录成功\",\"openid\":\""+openid+"\",\"is_login\":\""+is_login+"\",\"auth\":\""+user_auth+"\"}",
                            content_type='application/json',)
        else:
            return Response(_generate_json_message(False,"code 无效"))
        # return HttpResponse(json.dumps(json.loads(req.content)),content_type='application/json',)

# weixin 获取用户信息
@api_view(['POST'])
def weixin_gusi(request):
    if request.method == 'POST':
        appId = cf.get("WEIXIN", "weixin_appid")
        openid = request.POST['openid']
        try:
            sessionKey = WeixinSessionKey.objects.get(weixin_openid=openid).weixin_sessionkey
            encryptedData = request.POST['encryptedData']
            iv = request.POST['iv']
            pc = WXBizDataCrypt(appId, sessionKey)
            res_data = pc.decrypt(encryptedData, iv)
            phone_number = res_data["phoneNumber"]
            # 增加创建用户动作 openid phonenumber nickname
            try:
                # 用户登录时判断用户是否存在
                userinfo = UserInfo.objects.get(weixin_openid=openid)
                res_data["auth"]= userinfo.auth
            except UserInfo.DoesNotExist:
                # 不存在则创建新用户
                userinfo = UserInfo(weixin_openid=openid,
                                    phone_number=phone_number,
                                    auth="0")
                userinfo.save()
                res_data["auth"] = "0"
            return HttpResponse(json.dumps(res_data),content_type='application/json')
        except:
            pass


def __weixin_send_message(touser,date3,thing6,phrase1):
    # get access token
    APPID = cf.get("WEIXIN", "weixin_appid")
    SECRET = cf.get("WEIXIN", "weixin_secret")
    get_access_token_request_data = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+APPID+"&secret="+SECRET+""
    req_access = requests.get(get_access_token_request_data)
    access_token = json.loads(req_access.content)['access_token']
    body = {
            "access_token":access_token,
            "touser": touser,
            "template_id": cf.get("WEIXIN", "weixin_template_id"),
            "miniprogram_state": cf.get("WEIXIN", "miniprogram_state"),
            "data":{
                "date3": {
                    "value": date3
                },
                "thing6":{
                    "value": thing6
                },
                "phrase1":{
                    "value": phrase1
                }
            }

    }
    requst_data = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token="+access_token+""
    response = requests.post(requst_data, data = json.dumps(body))
    logger.info("通知用户 %s  内容为 %s  微信服务器返回结果为 %s" % (touser, json.dumps(body),response.content))
    return 0
