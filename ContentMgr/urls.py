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

app_name = 'ContentMgr'
urlpatterns = [
    # ex: /ContentMgr/logging
    url(r'^logging/$', views.logging, name='logging'),
    # ex: /ContentMgr/retrieve/
    url(r'^retrieve/$', views.retrieve, name='retrieve'),
    # ex: /ContentMgr/retrieve/poweron/
    url(r'^retrieve/poweron/$', views.retrieve_poweron, name='retrieve_poweron'),
    # ex: /ContentMgr/retrieve/map/
    url(r'^retrieve/map/$', views.retrieve_map, name='retrieve_map'),
    # ex: /ContentMgr/retrieve/input_sel/
    url(r'^retrieve/input_sel/$', views.retrieve_input_sel, name='retrieve_input_sel'),
    # ex: /ContentMgr/retrieve/mode/
    url(r'^retrieve/mode/$', views.retrieve_mode, name='retrieve_mode'),
    # ex: /ContentMgr/retrieve/environment/
    url(r'^retrieve/environment/$', views.retrieve_environment, name='retrieve_environment'),
]
