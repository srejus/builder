from django.db import models
from accounts.models import Account

# Create your models here.
class BookArcAppointment(models.Model):
    RECEIVED = 'RECEIVED'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'

    STATUS_CHOICES = (
        (RECEIVED,RECEIVED),
        (ACCEPTED,ACCEPTED),
        (REJECTED,REJECTED)
    )

    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    appointment_for = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='appointment_for') # architect
    booking_date = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=100,default='RECEIVED',choices=STATUS_CHOICES)

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
    price = models.FloatField(default=0.0)
    total_downloads = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)