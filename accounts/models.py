from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    USER_ROLES = (
        ('CUSTOMER','CUSTOMER'),
        ('ARCHITECT','ARCHITECT'),
        ('CONTRACTOR','CONTRACTOR'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    role = models.CharField(max_length=50,default='CUSTOMER',choices=USER_ROLES)
    email = models.EmailField()
    company_name = models.CharField(max_length=100,null=True,blank=True)
    domain = models.CharField(max_length=100,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)

    no_of_workers = models.IntegerField(default=1) # only for contractor

    def __str__(self):
        return str(self.first_name)+' '+str(self.last_name)


