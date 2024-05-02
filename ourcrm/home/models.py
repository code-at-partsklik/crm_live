from django.db import models
from django.contrib.auth.models import AbstractUser
from home.managers import *

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    user_role=models.CharField(max_length=100,null=True,blank=True,default='Sales')
    visible_password=models.CharField(max_length=254,null=True,blank=True)
    live_status=models.IntegerField(default=1,null=True,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self) -> str:
        return self.first_name 
    objects = CustomUserManager()

class roleList(models.Model):
    role_name=models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.role_name
    
class indiamartLead(models.Model):
    query_id=models.CharField(max_length=300,null=True,blank=True)
    lead_name=models.CharField(max_length=200,null=True,blank=True)
    contact=models.CharField(max_length=50,null=True,blank=True)
    email=models.CharField(max_length=150,null=True,blank=True)
    subject=models.CharField(max_length=150,null=True,blank=True)
    address=models.CharField(max_length=250,null=True,blank=True)
    product=models.CharField(max_length=150,null=True,blank=True)
    message=models.CharField(max_length=300,null=True,blank=True)
    enquery_time=models.CharField(max_length=200,null=True,blank=True)
    query_type=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self) -> str:
        return str(self.lead_name) +  str(self.subject)

class last_query(models.Model):
    last_request=models.CharField(max_length=100,null=True,blank=True)

