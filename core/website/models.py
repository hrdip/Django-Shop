from django.db import models
# Create your models here.

class ContactUsModel(models.Model):
    first_name = models.CharField(max_length=200, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    phone_number = models.CharField(max_length=12)
    subject = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_fullname(self): 
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        return self.email
    
    def __str__(self):
        return self.subject
    
    
        

class NewsLetterModel(models.Model):
    email = models.EmailField(blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.email
