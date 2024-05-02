from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.models import UserType
# Create your views here.


class DashboardHomeView(LoginRequiredMixin, View):
    # dispatch method, recognize with method are requested and  happend befor go to view or another functions
    def dispatch(self, request, *args, **kwargs):
        # recognize the user are admin or customer and redirect to the correct url
        if request.user.is_authenticated:
            if request.user.type == UserType.customer.value:
                return redirect(reverse_lazy('dashboard:customer:home'))
            if request.user.type == UserType.admin.value:
                return redirect(reverse_lazy('dashboard:admin:home'))
        else:
            return redirect(reverse_lazy('accounts:login'))

        return super().dispatch(request, *args, **kwargs)
