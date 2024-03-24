from django.db import models
from accounts.models import Account

# Create your models here.
class BookContractorAppointment(models.Model):
    RECEIVED = 'RECEIVED'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'

    STATUS_CHOICES = (
        (RECEIVED,RECEIVED),
        (ACCEPTED,ACCEPTED),
        (REJECTED,REJECTED)
    )
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    appointment_for = models.ForeignKey(Account,on_delete=models.CASCADE,
                                        related_name='appointment_for_contractor') # architect
    status = models.CharField(max_length=100,default='RECEIVED',choices=STATUS_CHOICES)
    booking_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return str(self.user)+" > "+str(self.appointment_for)