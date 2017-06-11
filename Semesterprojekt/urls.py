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
from MyA.views import get_staff
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

""" 
url(r'^staff/$', staff)
 r = raw String, wird nicht interpretiert
 ^ = beginnt String
 $ = end String
 staff = Methode aufrufen

"""

urlpatterns = (
    url(r'^admin/', admin.site.urls),
    url(r'^staff/', get_staff),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
)
