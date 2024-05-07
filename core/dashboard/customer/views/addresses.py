from django.views.generic import UpdateView, DeleteView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasCustomerAccessPermission
from dashboard.customer.forms import UserAddressForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from order.models import UserAddressModel
from django.shortcuts import redirect
from django.core.exceptions import FieldError
# Create your views here.


class CustomerAddressListView(HasCustomerAccessPermission, LoginRequiredMixin, ListView):
    template_name = 'dashboard/customer/addresses/address-list.html'

    # filters and get response
    def get_queryset(self):
        queryset = UserAddressModel.objects.filter(user=self.request.user)
        
        # get query parameters with self.request.GET.get("q") from url
        # := minimizing this code:  search_q=self.request.GET.get("q")    if search_q:     queryset = queryset.filter(title__icontains=search_q)
        # := اگر وجود داشت تخصیص بده python 3.8 and up supported
        if search_q := self.request.GET.get("q"):
            # we are filtering again that queryset in above
            # if search_q is existing filter by that (title__icontains=search_q)
            queryset = queryset.filter(title__icontains=search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    

class CustomerAddressCreateView(HasCustomerAccessPermission, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'dashboard/customer/addresses/address-create.html'
    form_class = UserAddressForm
    success_message = "address was successfully created"

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        # product model need User
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(reverse_lazy("dashboard:customer:address-edit", kwargs={"pk":form.instance.pk}))

    def get_success_url(self):
        return reverse_lazy("dashboard:customer:address-list")


class CustomerAddressEditView(HasCustomerAccessPermission, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/customer/addresses/address-edit.html'
    form_class = UserAddressForm
    success_message = "address was successfully updated"

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy("dashboard:customer:address-edit", kwargs={"pk":self.get_object().pk})


class CustomerAddressDeleteView(HasCustomerAccessPermission, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'dashboard/customer/addresses/address-delete.html'
    success_message = "address was successfully deleted"
    success_url = reverse_lazy("dashboard:customer:address-list")
    
    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)


