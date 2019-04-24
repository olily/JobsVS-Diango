"""JobsVS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import url,include
from rest_framework.documentation import include_docs_urls
# from django.contrib import admin
import xadmin
from JobsVS.settings import MEDIA_ROOT
from django.views.static import serve
# from goods.views_base import GoodsListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# router.register(r'goods',GoodsListViewSet)


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    # url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    #商品列表页
    url(r'^',include(router.urls)),
    url(r'docs/',include_docs_urls(title='招聘信息可视化'))
]
