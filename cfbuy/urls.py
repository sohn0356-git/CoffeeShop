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
    # url(r'^$', index, name='index'),  
    # url(r'^detail/$',TemplateView.as_view(template_name='cfproduct/product_detail.html'),name='detail'),
    # url(r'^cart/$',TemplateView.as_view(template_name='cfproduct/cart.html'),name='cart'),
    # url(r'^buy_page/$',TemplateView.as_view(template_name='cfproduct/buy_page.html'),name='buy_page'),
    # url(r'^order/$',TemplateView.as_view(template_name='cfproduct/order.html'),name='order'),
]
