"""proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from django.conf import settings
from django.contrib.auth import views as auth_views

from pelis import views

urlpatterns = [
    url(r'^ejercicios/',include('ejercicios.urls')),
    url(r'^pelis/',include('pelis.urls')),



    path('admin/', admin.site.urls),
    # # Uncomment the admin/doc line below to enable admin documentation:
    #  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #
    # # Uncomment the next line to enable the admin:
    #  url(r'^admin/', include(admin.site.urls)),


    # para tarea 9
    path('accounts/', include('allauth.urls')),
    path('', views.vista_crud, name='vamo'),
]
