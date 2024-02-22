from django.db import models
from accounts.models import Account

# Create your models here.
class BookArcAppointment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    appointment_for = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='appointment_for') # architect
    booking_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return str(self.user)+" > "+str(self.appointment_for)
    

class Works(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='work_cover')

    def __str__(self):
        return str(self.user)


class Plans(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='plan_cover')
    plan = models.FileField(upload_to='plan_file')

    def __str__(self):
        return str(self.user)