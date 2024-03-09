from django.db import models
from accounts.models import Account

# Create your models here.
class RentItems(models.Model):
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='rent_items')
    rent_per_day = models.FloatField()

    def __str__(self):
        return str(self.title)
    

class RentOrder(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='order_user')
    item = models.ForeignKey(RentItems,on_delete=models.CASCADE,related_name='order_item')
    quantity = models.IntegerField(default=1)
    name = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    no_of_days = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item.title) + " - "+ str(self.quantity)