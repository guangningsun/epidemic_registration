from django.contrib import admin
from epidemicapp import views
from django.conf.urls import include, url
from django.urls import path,re_path
from django.views.static import serve
from django.conf import settings
from AppModel import admin as appadmin
from django.views.generic.base import RedirectView

urlpatterns = [
    url('admin/', admin.site.urls),
    path('weixin_sns/<js_code>', views.weixin_sns),
    path('weixin_gusi/', views.weixin_gusi),
    
    re_path(r'^media/(?P<path>.+)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('asset/', views.asset_detail),
    path('asset/<int:cid>', views.asset_by_cid),
    path('userinfo/', views.userinfo_detail),
    # path('record_list/<int:sn>', views.epidemic_detail),
    path('record_list/', views.claim_detail),
    path('claim_asset/<int:weixin_id>', views.claim_asset),
    path('claim_asset/', views.claim_asset),
    path('commoditycategory/', views.commoditycategory_detail),
    path('get_approval_list/', views.get_approval_list),
    path('change_approval_status/', views.change_approval_status),

    path('get_category/', views.get_category),
    path('get_category_surplus/<int:cid>', views.get_category_surplus),
    path('get_supplier/<int:sn>', views.get_supplier),
    path('submit_user_info/', views.submit_user_info),
    path('get_user_info_by_wxid/<weixin_id>', views.get_user_info_by_wxid),
    path('submit_order/', views.submit_order),
    path('asset_by_cname/<cname>', views.asset_by_cname),
    path('get_all_order_info_list/<weixin_id>', views.get_all_order_info_list),
    
    

    
    
    
    # url(r'^favicon\.ico/pre>, RedirectView.as_view(url=r'static/favicon.ico')),

    
    


    
    
    
    

] 
 
