from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
)
from .models import ReviewModel
from django.urls import reverse_lazy
from .forms import SubmitReviewForm
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

class SubmitReviewView(LoginRequiredMixin, CreateView):
    http_method_names = ['post']
    model = ReviewModel
    form_class = SubmitReviewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        product = form.cleaned_data['product']

        messages.success(self.request,"دیدگاه شما با موفقیت ثبت گردید و پس از بررسی نمایش داده خواهد شد")
        return redirect(reverse_lazy('shop:product-detail', kwargs={"slug":product.slug}))
    
    def form_invalid(self,form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        # redirect to the same page
        return redirect(self.request.META.get('HTTP_REFERER'))
       
    def get_queryset(self):
        return ReviewModel.objects.filter(user=self.request.user)