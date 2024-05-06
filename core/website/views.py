from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from . models import ContactUsModel, NewsLetterModel
from .forms import ContactUsForm, NewsLetterForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
# Create your views here.


class IndexView(TemplateView):
    template_name = 'website/index.html'

class NewsLetterView(View):
    http_method_names = ['post']
    model = NewsLetterModel()
    form_class = NewsLetterForm

    def post(self, request):
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            # Process the form data
            email = form.cleaned_data['email']
            # Save the form data or perform any desired actions
            form.save()
            messages.add_message(request,messages.SUCCESS,'your ticket submitted successfully')  # Redirect to a success page
            return redirect(self.get_success_url())
        else:
            messages.add_message(request,messages.ERROR,'your ticket didnt submitted')
            return redirect('website:index')
    
    def get_success_url(self):
        return reverse_lazy('website:index')

class ContactUsView(View):
    template_name = 'website/contact.html'
    model = ContactUsModel

    def get(self, request):
        form = ContactUsForm()
        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            # Process the form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Save the form data or perform any desired actions
            form.save()
            messages.add_message(request,messages.SUCCESS,'your ticket submitted successfully')  # Redirect to a success page
        else:
            messages.add_message(request,messages.ERROR,'your ticket didnt submitted')
        context = {'form':form}
        return render(request, self.template_name, context)

class AboutView(TemplateView):
    template_name = 'website/about.html'