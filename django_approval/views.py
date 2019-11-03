# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	Approval,
)


class ApprovalCreateView(CreateView):

    model = Approval


class ApprovalDeleteView(DeleteView):

    model = Approval


class ApprovalDetailView(DetailView):

    model = Approval


class ApprovalUpdateView(UpdateView):

    model = Approval


class ApprovalListView(ListView):

    model = Approval

