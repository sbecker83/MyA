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
    # index
    url(r'^$', MyA.views.homesite, name='startseite'),

    # employee - overview, new, edit, delete
    url(r'^mitarbeiter/$', MyA.views.get_employee, name='mitarbeiterListe'),
    url(r'^mitarbeiter/neuerMA/$', MyA.views.details_employee, name='neuerMitarbeiter'),
    url(r'^mitarbeiter/editMa/(?P<pk>[0-9]+)/change//?$', MyA.views.details_employee, name='editMitarbeiter'),
    url(r'^mitarbeiter/editMa/(?P<pk>[0-9]+)/password//?$', MyA.views.set_password, name='setPasswordForUser'),
    url(r'^mitarbeiter/deleteMa/(?P<pk>[0-9]+)/?$', MyA.views.delete_employee, name='deleteMitarbeiter'),
    url(r'^mitarbeiter/export$', MyA.views.export_employees, name='exportMitarbeiter'),

    # user profil and pwd change of current user
    url(r'^profil/$', MyA.views.edit_profile, name='profil'),
    url(r'^password/$', MyA.views.change_password, name='setPasswordForUser'),
    url(r'^profil/toggleMa/(?P<pk>[0-9]+)/?$', MyA.views.toggle_employee_active, name='toggleMitarbeiter'),

    # calendar
    url(r'^kalender/?$', MyA.views.get_calendar, name='terminkalender'),
    url(r'^kalender/(?P<year>[0-9]+)/(?P<month>[0-9]+)/?$', MyA.views.get_calendar, name='terminkalender'),
    url(r'^kalender/neuerTermin/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/?$', MyA.views.details_calendar, name='neuerTermin'),
    url(r'^kalender/editTermin/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<pk>[0-9]+)/?$', MyA.views.details_calendar, name='editTermin'),

    # login / logout
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    # customer - overview, new, edit, delete
    url(r'^kunden/$', MyA.views.get_customer, name='kundenliste'),
    url(r'^kunden/neuerKD/$',  MyA.views.details_customer, name='neuerkunde'),
    url(r'^kunden/editKD/(?P<pk>[0-9]+)/?$',  MyA.views.details_customer, name='editkunde'),
    url (r'^kunden/deleteKD/(?P<pk>[0-9]+)/(?P<status>[0-9]+)/?$', MyA.views.delete_customer, name='deletekunde'),
    url(r'^kunden/export$', MyA.views.export_customers, name='exportKunde'),

    # contact - overview, new, edit, delete
    url(r'^ansprechpartner/(?P<fk>[0-9]+)/?$', MyA.views.get_contact, name='ansprechpartnerliste'),
    url(r'^ansprechpartner/neuerAP/(?P<fk>[0-9]+)/?$', MyA.views.details_contact, name='neueransprechpartner'),
    url(r'^ansprechpartner/editAP/(?P<pk>[0-9]+)/(?P<fk>[0-9]+)/?$', MyA.views.details_contact, name='editansprechpartner'),
    url(r'^ansprechpartner/deleteAP/(?P<status>[0-9]+)/(?P<pk>[0-9]+)/(?P<fk>[0-9]+)/?$', MyA.views.delete_contact, name='deleteansprechpartner'),
    url(r'^ansprechpartner/export$', MyA.views.export_contacts, name='exportAnsprechpartner'),

    # note - overview, new, edit, delete
    url(r'^notiz/$', MyA.views.get_notes, name='notizliste'),
    url(r'^notiz/neuerNO/$', MyA.views.details_note, name='neuenotiz'),
    url(r'^notiz/editNO/(?P<pk>[0-9]+)/?$', MyA.views.details_note, name='editnotiz'),
    url(r'^notiz/deleteNO/(?P<pk>[0-9]+)/?$', MyA.views.delete_note, name='deletenotiz'),
    url(r'^notiz/export$', MyA.views.export_notes, name='exportNotiz'),


)
