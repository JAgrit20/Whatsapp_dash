# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Whatsapp_data(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.CharField(max_length=10)
    convesation_id = models.CharField(max_length=100)
    our_phone_number = models.CharField(max_length=100)
    our_phone_number_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=100)
    msg_id = models.CharField(max_length=100)
    response_from_user = models.TextField()
    message_type = models.CharField(max_length=100)
    response_from_us = models.TextField()
    New_user_check = models.BooleanField(null=True, blank=True)
    We_responded_check = models.BooleanField(null=True, blank=True)
