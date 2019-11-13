# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^admin/', include('django_approval.urls', namespace='django_approval')),
]
