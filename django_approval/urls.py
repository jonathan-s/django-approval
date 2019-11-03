# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


app_name = 'django_approval'
urlpatterns = [
    url(
        regex="^Approval/~create/$",
        view=views.ApprovalCreateView.as_view(),
        name='Approval_create',
    ),
    url(
        regex="^Approval/(?P<pk>\d+)/~delete/$",
        view=views.ApprovalDeleteView.as_view(),
        name='Approval_delete',
    ),
    url(
        regex="^Approval/(?P<pk>\d+)/$",
        view=views.ApprovalDetailView.as_view(),
        name='Approval_detail',
    ),
    url(
        regex="^Approval/(?P<pk>\d+)/~update/$",
        view=views.ApprovalUpdateView.as_view(),
        name='Approval_update',
    ),
    url(
        regex="^Approval/$",
        view=views.ApprovalListView.as_view(),
        name='Approval_list',
    ),
	]
