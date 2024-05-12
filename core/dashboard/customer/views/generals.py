from django.views.generic import  TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasCustomerAccessPermission
from shop.models import WishlistProductModel
# Create your views here.


class CustomerDashboardHomeView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'dashboard/customer/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_products"] = WishlistProductModel.objects.filter(user=self.request.user).count()
        return context