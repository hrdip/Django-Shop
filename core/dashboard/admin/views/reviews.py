from django.views.generic import (
    UpdateView,
    ListView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from dashboard.admin.forms import ReviewForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from review.models import ReviewModel, ReviewStatusType
from django.core.exceptions import FieldError
# Create your views here.

class AdminReviewListView(HasAdminAccessPermission, LoginRequiredMixin, ListView):
    template_name = 'dashboard/admin/reviews/admin-review-list.html'
    paginate_by = 10 

    def get_paginate_by(self, queryset):
        # if page_size are existing return it else return paginate_by
        return self.request.GET.get('page_size', self.paginate_by)

    # filters and get response
    def get_queryset(self):
        queryset = ReviewModel.objects.all()
        
        # get query parameters with self.request.GET.get("q") from url
        # := minimizing this code:  search_q=self.request.GET.get("q")    if search_q:     queryset = queryset.filter(title__icontains=search_q)
        # := اگر وجود داشت تخصیص بده python 3.8 and up supported
        if search_q := self.request.GET.get("q"):
            # we are filtering again that queryset in above
            # if search_q is existing filter by that (title__icontains=search_q)
            queryset = queryset.filter(product__title__icontains=search_q)

        if status := self.request.GET.get("status"):
            queryset = queryset.filter(status=status)

        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_products"] = self.get_queryset().count()
        context["status_types"] = ReviewStatusType.choices
        return context
    

class AdminReviewEditView(HasAdminAccessPermission, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/admin/reviews/admin-review-edit.html'
    queryset = ReviewModel.objects.all()
    form_class = ReviewForm
    success_message = "review was successfully updated"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:admin-review-edit", kwargs={'pk': self.kwargs.get('pk')})
