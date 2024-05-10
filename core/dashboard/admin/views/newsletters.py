from django.views.generic import ListView , DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from django.core.exceptions import FieldError
from website.models import NewsLetterModel
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

class AdminNewsletterListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/newsletters/admin-newsletter-list.html"
    paginate_by = 10
    ordering = "-created_date"
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size',self.paginate_by)

    def get_queryset(self):
        queryset = NewsLetterModel.objects.all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(email__icontains=search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_result"] = self.get_queryset().count()
        return context


class AdminNewsletterDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    title = "حذف خبرنامه"
    template_name = "dashboard/admin/newsletters/admin-newsletter-delete.html"
    success_url = reverse_lazy("dashboard:admin:newsletter-list")
    success_message = "عضو مورد نظر با موفقیت حذف شد"

    def get_queryset(self):
        return NewsLetterModel.objects.all()
    

