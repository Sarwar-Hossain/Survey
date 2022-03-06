from django.utils import timezone
from django.db import models
from datetime import datetime


# Create your models here.

class ShopUser(models.Model):
    objects = None

    shop_id = models.IntegerField(blank=False, null=False, default=None)
    shop_name = models.CharField(max_length=150, null=False, blank=False, default='')
    user_name = models.CharField(max_length=100, blank=False, null=False)
    mobile_no = models.CharField(max_length=15, null=True)
    is_user_active = models.BooleanField(null=False, default=True)
    email = models.EmailField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=500, blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Customer(models.Model):
    objects = None

    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    membership_no = models.IntegerField(null=False, blank=False)
    in_voice_no = models.IntegerField(null=False, blank=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    contact_no = models.CharField(max_length=15, null=True)
    date_of_birth = models.DateField(blank=False, null=False)
    marital_status = models.CharField(max_length=100, blank=True, null=True, default='')
    address = models.CharField(max_length=200, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True)


class CustomerFeedback(models.Model):
    objects = None

    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)

    question_1 = models.BooleanField(null=False, default=True)
    question_2 = models.BooleanField(null=False, default=True)
    question_3 = models.BooleanField(null=False, default=True)
    question_4 = models.BooleanField(null=False, default=True)
    question_5 = models.BooleanField(null=False, default=True)
    question_6 = models.TextField(blank=False, null=False)
    question_7 = models.TextField(blank=False, null=False)
    question_8 = models.TextField(blank=False, null=False)
    question_9 = models.TextField(blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True, null=True)

