from django.db import models


# Create your models here.

class Customer(models.Model):
    objects = None

    customer_id = models.IntegerField(null=False, blank=False)
    membership_no = models.IntegerField(null=False, blank=False)
    in_voice_no = models.IntegerField(null=False, blank=False)
    CATEGORIES = (
        (1, 'Category one'),
        (2, 'Category two'),
        (3, 'Category three'),
    )
    category = models.IntegerField(choices=CATEGORIES)
    title = models.CharField(max_length=100, blank=False, null=False)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)

