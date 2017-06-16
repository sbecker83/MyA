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
    url(r'^$', MyA.views.homesite, name='startseite'),
    url(r'^mitarbeiter/$', MyA.views.get_employees, name='mitarbeiter'),
    url(r'^mitarbeiter/neuerMA/$', MyA.views.new_employee, name='newEmployee'),
    url(r'^mitarbeiter/editMa/(?P<pk>[0-9]+)/change//?$', MyA.views.new_employee, name='editEmployee'),
    url(r'^mitarbeiter/editMa/(?P<pk>[0-9]+)/password//?$', MyA.views.set_password, name='setPasswordForUser'),
    url(r'^profil/$', MyA.views.myProfile, name='profil'),
    url(r'^kalender/$', MyA.views.calendar, name='terminkalender'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url (r'^kunden/$', MyA.views.get_customer, name='kundenliste'),
    url (r'^kunden/neuerKD/$',  MyA.views.details_customer, name='neuerkunde'),
    url (r'^kunden/editKD/(?P<pk>[0-9]+)/?$',  MyA.views.details_customer, name='editkunde'),
    url (r'^kunden/deleteKD/(?P<pk>[0-9]+)/?$',  MyA.views.delete_customer, name='deletekunde'),
    url (r'^ansprechpartner/$', MyA.views.get_contact, name='ansprechpartnerliste'),
    url (r'^ansprechpartner/neuerAP/$', MyA.views.details_contact, name='neueransprechpartner'),
    url (r'^ansprechpartner/editAP/(?P<pk>[0-9]+)/?$', MyA.views.details_contact, name='editansprechpartner'),
    url (r'^ansprechpartner/deleteAP/(?P<pk>[0-9]+)/?$', MyA.views.delete_contact, name='deleteansprechpartner'),
    url (r'^notiz/$', MyA.views.get_notes, name='notizliste'),
    url (r'^notiz/neuerNO/$', MyA.views.details_note, name='neuenotiz'),
    url (r'^notiz/editNO/(?P<pk>[0-9]+)/?$', MyA.views.details_note, name='editnotiz'),
    url (r'^notiz/deleteNO/(?P<pk>[0-9]+)/?$', MyA.views.delete_note, name='deletenotiz')

)
