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
  

] 
 
