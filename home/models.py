from django.db import models

# Create your models here.
class RentItems(models.Model):
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='rent_items')
    rent_per_day = models.FloatField()

    def __str__(self):
        return str(self.title)