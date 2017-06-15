"""Semesterprojekt URL Configuration

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
from django.contrib.auth import views as auth_views

import MyA.views

admin.autodiscover()

urlpatterns = (
    url(r'^admin/', admin.site.urls),
    url(r'^startseite/$', MyA.views.homesite, name='startseite'),
    url(r'^mitarbeiter/$', MyA.views.get_staff, name='mitarbeiter'),
    url(r'^mitarbeiter/neuerMA/$', MyA.views.new_Staff, name='newStaff'),
    url(r'^profil/$', MyA.views.myProfile, name='profil'),
    url(r'^kalender/$', MyA.views.calendar, name='terminkalender'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url (r'^kunden/$', MyA.views.get_customer, name='kundenliste'),
    url (r'^kunden/neuerKD/$',  MyA.views.new_customer, name='neuerkunde'),
    url (r'^ansprechpartner/$', MyA.views.get_contact, name='ansprechpartnerliste'),
    url (r'^ansprechpartner/neuerAP/$', MyA.views.new_contact, name='neueransprechpartner')
)
