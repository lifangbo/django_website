"""firstProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

from django.conf.urls.static import static

from . import views

app_name = 'AAA'
urlpatterns = [
    # ex: /AAA/user
    url(r'^user/$', views.user, name='user'),
    # ex: /AAA/user/<ID>
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user_id, name='user_id'),
    # ex: /AAA/user/<ID>/password
    url(r'^user/(?P<user_id>[0-9]+)/password/$', views.password, name='password'),
    # ex: /AAA/user/login
    url(r'^user/login/$', views.login, name='login'),
    # ex: /AAA/user/login
    url(r'^user/logout/$', views.logout, name='logout'),
    # ex: /AAA/user/add
    url(r'^user/add/$', views.user_add, name='user_add'),
    # ex: /AAA/user/userInfo
    url(r'^user/userInfo/$', views.user_info, name='user_info'),
]
