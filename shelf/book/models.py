# -*- coding: UTF-8 -*-
from django.db import models
from django.urls import reverse

# Create your models here.
class Book(models.Model):
    ISBN = models.CharField(max_length = 30)
    IsBorrowed = models.BooleanField()
    BookName = models.CharField(max_length = 250)
    Author = models.CharField(max_length = 100,default = "未知")
    Translator = models.CharField(max_length = 100,default = "无")
    Publisher = models.CharField(max_length = 100,default = "未知")
    DevoterName = models.CharField(max_length = 100,default = "未知")
    
    def get_absolute_urls(self):
        return reverse(
            "book:detail",
            kwargs={ 'pk': self.pk}
        )