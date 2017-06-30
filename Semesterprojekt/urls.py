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
    # index/dashboard
    url(r'^$', MyA.views.dashboard, name='dashboard'),

    # employee - list, new, edit, toggle, export
    url(r'^employee/$', MyA.views.list_employees, name='list_employees'),
    url(r'^employee/new/$', MyA.views.detail_employee, name='new_employee'),
    url(r'^employee/edit/(?P<pk>[0-9]+)/change//?$', MyA.views.detail_employee, name='edit_employee'),
    url(r'^employee/edit/(?P<pk>[0-9]+)/password//?$', MyA.views.set_password, name='set_password_user'),
    url(r'^employee/toggle_status/(?P<pk>[0-9]+)/?$', MyA.views.toggle_employee_active, name='toggle_employee_status'),
    url(r'^employee/export$', MyA.views.export_employees, name='export_employees'),

    # user profil and pwd change of current user
    url(r'^profile/$', MyA.views.edit_profile, name='profile'),
    url(r'^password/$', MyA.views.change_password, name='set_password_user'),

    # calendar
    url(r'^calendar/?$', MyA.views.get_calendar, name='calendar'),
    url(r'^calendar/(?P<year>[0-9]+)/(?P<month>[0-9]+)/?$', MyA.views.get_calendar, name='calendar'),
    url(r'^calendar/event/new/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/?$', MyA.views.detail_event, name='new_event'),
    url(r'^calendar/event/edit/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<pk>[0-9]+)/?$', MyA.views.detail_event_members, name='edit_event'),
    url(r'^calendar/event/delete/(?P<pk>[0-9]+)/?$', MyA.views.delete_event, name='delete_event'),
    url(r'^calendar/event/member/internal/delete/(?P<pk>[0-9]+)/?$', MyA.views.delete_event_member_internal, name='delete_event_member_internal'),
    url(r'^calendar/event/member/external/delete/(?P<pk>[0-9]+)/?$', MyA.views.delete_event_member_external, name='delete_event_member_external'),

    # login / logout
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    # customer - list, new, edit, delete, export
    url(r'^customer/$', MyA.views.list_customers, name='list_customers'),
    url(r'^customer/new/$', MyA.views.detail_customer, name='new_customer'),
    url(r'^customer/edit/(?P<pk>[0-9]+)/?$', MyA.views.detail_customer, name='edit_customer'),
    url(r'^customer/delete/(?P<pk>[0-9]+)/(?P<is_delete>[0-1])/?$', MyA.views.delete_customer, name='delete_customer'),
    url(r'^customer/export$', MyA.views.export_customers, name='export_customers'),

    # contact - overview, new, edit, delete, export
    url(r'^contact/(?P<fk>[0-9]+)/?$', MyA.views.list_contacts, name='list_contacts'),
    url(r'^contact/neuer/(?P<fk>[0-9]+)/?$', MyA.views.details_contact, name='new_contact'),
    url(r'^contact/edit/(?P<pk>[0-9]+)/(?P<fk>[0-9]+)/?$', MyA.views.details_contact, name='edit_contact'),
    url(r'^contact/delete/(?P<is_delete>[0-9]+)/(?P<pk>[0-9]+)/(?P<fk>[0-9]+)/?$', MyA.views.delete_contact, name='delete_contact'),
    url(r'^contact/export$', MyA.views.export_contacts, name='export_contacts'),

    # note - overview, new, edit, delete, export
    url(r'^note/$', MyA.views.list_notes, name='list_notes'),
    url(r'^note/new/$', MyA.views.detail_note, name='new_note'),
    url(r'^note/edit/(?P<pk>[0-9]+)/?$', MyA.views.detail_note, name='edit_note'),
    url(r'^note/delete/(?P<pk>[0-9]+)/?$', MyA.views.delete_note, name='delete_note'),
    url(r'^note/export$', MyA.views.export_notes, name='export_notes'),


)
