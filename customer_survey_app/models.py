from django.db import models


# Create your models here.

class ShopUser(models.Model):
    objects = None

    shop_id = models.IntegerField(blank=False, null=False, default=None)
    shop_name = models.CharField(max_length=150, null=False, blank=False, default='')
    user_name = models.CharField(max_length=100, blank=False, null=False)
    mobile_no = models.CharField(max_length=15, null=True)
    is_user_active = models.BooleanField(null=False, default=True)
    email = models.EmailField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=100, null=False)
    created_time = models.DateTimeField(auto_now=False, null=True)
    created_by = models.CharField(max_length=100, blank=False, null=False, default='')
    updated_time = models.DateTimeField(auto_now=False, null=True)
    updated_by = models.CharField(max_length=100, blank=False, null=False, default='')


class Category(models.Model):
    objects = None

    category_name = models.CharField(max_length=100)


class Customer(models.Model):
    objects = None

    membership_no = models.IntegerField(null=True, blank=True)
    in_voice_no = models.IntegerField(null=False, blank=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    marital_status = models.CharField(max_length=100, blank=True, null=True, default='')
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=100, blank=False, null=False, default='')


class CustomerFeedback(models.Model):
    objects = None

    question_1 = models.BooleanField(null=False, default=True)
    question_2 = models.TextField(blank=False, null=False)
    question_3 = models.TextField(blank=False, null=False)
    question_4 = models.BooleanField(null=False, default=True)
    question_5 = models.BooleanField(null=False, default=True)
    question_6 = models.TextField(blank=False, null=False)
    question_7 = models.TextField(blank=False, null=False)
    question_8 = models.TextField(blank=False, null=False)
    question_9 = models.TextField(blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=100, blank=False, null=False, default='')
    membership_no = models.IntegerField(null=True, blank=True)
    customer_name = models.CharField(max_length=100, blank=False, null=False, default='')
