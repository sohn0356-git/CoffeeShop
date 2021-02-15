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
from cfuser.views import *
from cfbuy.views import show_graph
from django.conf import settings
from django.conf.urls.static import static

app_name = 'cfuser'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^graph/$', show_graph, name='graph'),
    url(r'^cart/$',cart,name='cart'),
    url(r'^about/$',TemplateView.as_view(template_name='map.html'),name='about'),
    url(r'^profile/$',profile,name='profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
