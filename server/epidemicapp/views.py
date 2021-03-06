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
from django.db.models import Max 


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

# 更新入住用户信息
@api_view(['POST'])
def update_family_info(request):
    if request.method == 'POST':
        try:
            id_num = request.POST['id_num']
            room = request.POST['room']
            hotel = request.POST['hotel']
            currenttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            CheckInfo.objects.filter(id_num=id_num).update(room=room,hotel=hotel)
            # 获取家庭账号
            fi = CheckInfo.objects.filter(id_num=id_num)[0].family_id
            # 遍历家庭id下所有人是否已分配房间
            checkinfo_list = CheckInfo.objects.filter(family_id=fi)
            checkin_status = "已分配" # 0未分配 1已分配
            for i in checkinfo_list:
                if i.room == '未分配':
                    checkin_status = "未分配"
            CheckInfo.objects.filter(id_num=id_num).update(checkin_status=checkin_status)
            # 通知户主房间已分配
            try:
                ci  = CheckInfo.objects.get(id_num=id_num)
                ui = UserInfo.objects.get(phone_number = ci.family_tel_num)
                ret1 = __weixin_send_message(ui.weixin_openid, currenttime ,room ,checkin_status,"入住已分配")
            except:
                pass
            res_json = {"error": 0,"msg": {"更新入住信息成功"}}
            return Response(res_json)
        except:
            res_json = {"error": 1,"msg": {"更新入住信息失败"}}
            return Response(res_json)



# 获取所有用户信息
@api_view([ 'GET'])
def get_all_family_info(request):
    if request.method == 'GET':
        # 定义家庭信息数组
        family_info_list = []
        # 获取家庭手机列表
        family_tel_num_all = CheckInfo.objects.values('family_tel_num').distinct()
        # 根据家庭手机列表拼接每个家庭的json数据
        for ftl in family_tel_num_all:
            checkinset = CheckInfo.objects.filter(family_tel_num=ftl['family_tel_num'])
            serializer = CheckinSerializer(checkinset, many=True)
            family_member_list_array = []
            for i in range (0,len(serializer.data)):
                family_member_info = {}
                family_member_info["name"] = serializer.data[i]["name"]
                family_member_info["gender"] = serializer.data[i]["gender"]
                family_member_info["age"] = serializer.data[i]["age"]
                family_member_info["nation"] = serializer.data[i]["nation"]
                family_member_info["id_num"] = serializer.data[i]["id_num"]
                family_member_info["tel_num"] = serializer.data[i]["tel_num"]
                family_member_info["address"] = serializer.data[i]["address"]
                family_member_info["work_place"] = serializer.data[i]["work_place"]
                family_member_info["has_disease_radio"] = serializer.data[i]["has_disease_radio"]
                family_member_info["disease_name"] = serializer.data[i]["disease_name"]
                family_member_info["medicine_name"] = serializer.data[i]["medicine_name"]
                family_member_info["has_take_medicine_radio"] = serializer.data[i]["has_take_medicine_radio"]
                family_member_info["room"] = serializer.data[i]["room"]
                family_member_info["hotel"] = serializer.data[i]["hotel"]
                family_member_list_array.append(family_member_info)

            # 拼接家庭json
            family_info = { "family_contact_name" :serializer.data[0]["family_contact_name"] ,
                                        "tel_num" :serializer.data[0]["family_tel_num"] ,
                                        "family_address" :serializer.data[0]["family_address"] ,
                                        "registerTime" :serializer.data[0]["registerTime"] ,
                                        "checkin_status" :serializer.data[0]["checkin_status"] ,
                                        "family_member_num" :serializer.data[0]["family_member_num"] ,
                                        "family_id": serializer.data[0]["family_id"],
                                        "family_member_list": family_member_list_array 
                                        } 
            # 放进家庭数组    
            family_info_list.append(family_info)
        # 拼接返回json信息
        res_json = {"error": 0,"msg": family_info_list }
        return Response(res_json)


# 通过手机号模糊查询家庭信息
@api_view(['GET'])
def fuzzy_query(request,tel_num):
    if request.method == 'GET':
        if tel_num.strip()!="":
            checkinset = CheckInfo.objects.filter(family_tel_num__icontains=tel_num)
            serializer = CheckinSerializer(checkinset, many=True)
            family_member_list_array = []
            for i in range (0,len(serializer.data)):
                family_member_info = {}
                family_member_info["name"] = serializer.data[i]["name"]
                family_member_info["gender"] = serializer.data[i]["gender"]
                family_member_info["age"] = serializer.data[i]["age"]
                family_member_info["nation"] = serializer.data[i]["nation"]
                family_member_info["id_num"] = serializer.data[i]["id_num"]
                family_member_info["tel_num"] = serializer.data[i]["tel_num"]
                family_member_info["address"] = serializer.data[i]["address"]
                family_member_info["work_place"] = serializer.data[i]["work_place"]
                family_member_info["has_disease_radio"] = serializer.data[i]["has_disease_radio"]
                family_member_info["disease_name"] = serializer.data[i]["disease_name"]
                family_member_info["medicine_name"] = serializer.data[i]["medicine_name"]
                family_member_info["has_take_medicine_radio"] = serializer.data[i]["has_take_medicine_radio"]
                family_member_info["room"] = serializer.data[i]["room"]
                family_member_info["hotel"] = serializer.data[i]["hotel"]
                family_member_list_array.append(family_member_info)

            res_json = {"error": 0,"msg": {
                        "family_info": { "family_contact_name" :serializer.data[0]["family_contact_name"] ,
                                        "tel_num" :serializer.data[0]["family_tel_num"] ,
                                        "family_address" :serializer.data[0]["family_address"] ,
                                        "registerTime" :serializer.data[0]["registerTime"] ,
                                        "checkin_status" :serializer.data[0]["checkin_status"] ,
                                        "family_member_num" :serializer.data[0]["family_member_num"] ,
                                        "family_id": serializer.data[0]["family_id"],
                                        "family_member_list": family_member_list_array 
                                        } 
                        }}
            return Response(res_json)
        else:
            res_json = {"error": 1,"msg": "查询内容为空"}
            return Response(res_json)


# 创建入住用户信息
@api_view([ 'POST'])
def create_family_info(request):
    if request.method == 'POST':
        # 收到所有家庭登记参数
        # 拆分公共参数部分
        try:
            family_contact_name = request.POST['family_contact_name']
            family_tel_num = request.POST['family_tel_num']
            # 检查该手机号用户是否存在，如果存在则更新
            ci = CheckInfo.objects.filter(family_tel_num=family_tel_num)
            if ci.exists():
                family_address = request.POST['family_address']
                # 对其他成员list进行save操作
                checkin_status = "未分配" # 0未分配 1已分配
                family_member_num = request.POST['family_member_num']
                family_member_list = request.POST['family_member_list']
                # 拿到家庭其他成员list
                for family_member in json.loads(family_member_list):
                    CheckInfo.objects.filter(id_num=family_member["id_num"]).update(
                                        family_member_num = family_member_num,
                                        name = family_member["name"],
                                        gender = family_member["gender"],
                                        age = family_member["age"],
                                        nation = family_member["nation"],
                                        tel_num = family_member["tel_num"],
                                        address = family_member["address"],
                                        work_place = family_member["work_place"],
                                        has_disease_radio = family_member["has_disease_radio"],
                                        disease_name = family_member["disease_name"],
                                        medicine_name = family_member["medicine_name"],
                                        has_take_medicine_radio = family_member["has_take_medicine_radio"],
                                        room = "(未分配)",
                                        hotel = "(未分配)",
                    )
            else:
                family_address = request.POST['family_address']
                registerTime= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 对其他成员list进行save操作，自动生成family id 生成创建注册时间
                checkin_status = "未分配" # 0未分配 1已分配
                family_member_num = request.POST['family_member_num']
                # family_id = int(time.time())
                family_id = "A1"
                try:
                    family_id = (("A%s") % ( CheckInfo.objects.all().aggregate(Max('id'))["id__max"]+1))
                except:
                    pass
                family_member_list = request.POST['family_member_list']
                # 拿到家庭其他成员list
                for family_member in json.loads(family_member_list):
                    checkin = CheckInfo(family_contact_name=family_contact_name,
                                        family_tel_num = family_tel_num,
                                        family_address = family_address,
                                        registerTime =registerTime,
                                        checkin_status =checkin_status,
                                        family_member_num = family_member_num,
                                        family_id = family_id,
                                        name = family_member["name"],
                                        gender = family_member["gender"],
                                        age = family_member["age"],
                                        nation = family_member["nation"],
                                        id_num = family_member["id_num"],
                                        tel_num = family_member["tel_num"],
                                        address = family_member["address"],
                                        work_place = family_member["work_place"],
                                        has_disease_radio = family_member["has_disease_radio"],
                                        disease_name = family_member["disease_name"],
                                        medicine_name = family_member["medicine_name"],
                                        has_take_medicine_radio = family_member["has_take_medicine_radio"],
                                        room = "未分配",
                                        hotel = "未分配",
                    )
                    checkin.save()
            res_json = {"error": 0,"msg": {"创建入住信息成功"}}
            return Response(res_json)
        except:
            res_json = {"error": 1,"msg": {"创建入住信息失败"}}
            return Response(res_json)


# 解除隔离
@api_view(['POST'])
def release_isolation(request):
    if request.method == 'POST':
        try:
            family_id = request.POST['family_id']
            CheckInfo.objects.filter(family_id=family_id).delete()
            res_json = {"error": 0,"msg": {"成功解除隔离"}}
            return Response(res_json)
        except:
            res_json = {"error": 1,"msg": {"解除隔离失败"}}
            return Response(res_json)

# 获取家庭信息
@api_view(['GET', 'POST'])
def get_family_info(request,tel_num):
    if request.method == 'GET':
        try:
            checkinset = CheckInfo.objects.filter(family_tel_num=tel_num)
            serializer = CheckinSerializer(checkinset, many=True)
            family_member_list_array = []
            for i in range (0,len(serializer.data)):
                family_member_info = {}
                family_member_info["name"] = serializer.data[i]["name"]
                family_member_info["gender"] = serializer.data[i]["gender"]
                family_member_info["age"] = serializer.data[i]["age"]
                family_member_info["nation"] = serializer.data[i]["nation"]
                family_member_info["id_num"] = serializer.data[i]["id_num"]
                family_member_info["tel_num"] = serializer.data[i]["tel_num"]
                family_member_info["address"] = serializer.data[i]["address"]
                family_member_info["work_place"] = serializer.data[i]["work_place"]
                family_member_info["has_disease_radio"] = serializer.data[i]["has_disease_radio"]
                family_member_info["disease_name"] = serializer.data[i]["disease_name"]
                family_member_info["medicine_name"] = serializer.data[i]["medicine_name"]
                family_member_info["has_take_medicine_radio"] = serializer.data[i]["has_take_medicine_radio"]
                family_member_info["room"] = serializer.data[i]["room"]
                family_member_info["hotel"] = serializer.data[i]["hotel"]
                family_member_list_array.append(family_member_info)

            res_json = {"error": 0,"msg": {
                        "family_info": { "family_contact_name" :serializer.data[0]["family_contact_name"] ,
                                        "tel_num" :serializer.data[0]["family_tel_num"] ,
                                        "family_address" :serializer.data[0]["family_address"] ,
                                        "registerTime" :serializer.data[0]["registerTime"] ,
                                        "checkin_status" :serializer.data[0]["checkin_status"] ,
                                        "family_member_num" :serializer.data[0]["family_member_num"] ,
                                        "family_id": serializer.data[0]["family_id"],
                                        "family_member_list": family_member_list_array 
                                        } 
                        }}
            return Response(res_json)
        except:
            res_json = {"error": 1,"msg": {"获取信息失败"}}
            return Response(res_json)
    # elif request.method == 'POST':
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         res_json = {"error": 0,"msg": {
    #                 "user_info": serializer.data }}
    #         return Response(res_json, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 通过微信id获取用户信息
@api_view(['GET'])
def get_user_info_by_wxid(request,weixin_id):
    if request.method == 'GET':
        userset = UserInfo.objects.filter(weixin_openid=weixin_id)
        serializer = UserInfoSerializer(userset, many=True)
        res_json = {"error": 0,"msg": {
                    "user_info": serializer.data }}
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
                # wsk = WeixinSessionKey.objects.get(weixin_openid=openid)
                # wsk.weixin_sessionkey = session_key
                # wsk.save()
                WeixinSessionKey.objects.filter(weixin_openid=openid).update(weixin_sessionkey = session_key)
                userinfo = UserInfo.objects.get(weixin_openid=openid)
                # 增加用户是否已登录
                is_login = "1"
                user_auth = userinfo.auth
            #except WeixinSessionKey.DoesNotExist:
            except :
                cwsk = WeixinSessionKey(weixin_openid=openid,weixin_sessionkey=session_key)
                cwsk.save()
                #WeixinSessionKey.objects.filter(weixin_openid=openid).update(weixin_sessionkey=session_key)
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
            # res_data["auth"] = "0"
            # return HttpResponse(json.dumps(res_data),content_type='application/json')


def __weixin_send_message(touser,date3,thing6,phrase1,name1):
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
                "thing4":{
                    "value": thing6
                },
                "phrase2":{
                    "value": phrase1
                },
                "name1":{
                    "value": name1
                }
            }

    }
    requst_data = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token="+access_token+""
    response = requests.post(requst_data, data = json.dumps(body))
    logger.info("通知用户 %s  内容为 %s  微信服务器返回结果为 %s" % (touser, json.dumps(body),response.content))
    return 0
