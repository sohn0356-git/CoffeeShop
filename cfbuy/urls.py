"""CoffeeShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.views.generic import TemplateView

from cfbuy.views import *

app_name = 'cfbuy'

urlpatterns = [
    # url(r'^test/$',TemplateView.as_view(template_name='cfproduct/test.html'),name='test'),
    url(r'^detail/$',TemplateView.as_view(template_name='cfbuy/_detail.html'),name='detail'),
    url(r'^cart/$',TemplateView.as_view(template_name='cfbuy/cart.html'),name='cart'),
    url(r'^buy_page/$',TemplateView.as_view(template_name='cfbuy/buy_page.html'),name='buy_page'),
    url(r'^order/$',order_list,name='order_list'),
    url(r'^complete/$',buy_complete,name='buy_complete'),
    url(r'^graph/$',show_graph,name='graph'),
    url(r'^kakao/$',kakaopay,name='kakao_pay'),
    url(r'^approve/$',approval,name='approve'),
    url(r'^cancel/$',TemplateView.as_view(template_name='cfbuy/payCancel.html'),name='cancel'),
    url(r'^fail/$',TemplateView.as_view(template_name='cfbuy/payFail.html'),name='fail'),
]
