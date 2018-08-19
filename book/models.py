# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Book(models.Model):
    ISBN = models.CharField(max_length = 30)
    IsBorrowed = models.BooleanField()
    BookName = models.CharField(max_length = 250)
    FrontPage = models.CharField (max_length = 400, default = 'static\no_frontpage.png')
    Author = models.CharField(max_length = 100,default = "未知")
    Translator = models.CharField(max_length = 100,default = "无")
    Publisher = models.CharField(max_length = 100,default = "未知")
    Devoter = models.ForeignKey(User, null = True,blank = True,on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=1)
    
     
    def get_absolute_urls(self): 
        return reverse(
            "book:detail", 
            kwargs={ 'pk': self.pk}
        )

class BorrowRecord(models.Model):
    Borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    BookBorrowed = models.ForeignKey(Book, null = True, on_delete = models.CASCADE)
    BeginTime = models.DateField(auto_now_add = True)

