# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Book(models.Model):
    ISBN = models.CharField(max_length = 30)
    BookName = models.CharField(max_length = 250)
    FrontPage = models.CharField (max_length = 400, default = 'static/no_frontpage.png')
    Author = models.CharField(max_length = 100,default = "未知")
    Translator = models.CharField(max_length = 100,default = "无")
    Publisher = models.CharField(max_length = 100,default = "未知")
    # devoter still exsits, though it will not be displayed, it would help me edit the template... 
    Devoter = models.ForeignKey(User, null = True,blank = True,on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=1)
    Introduction = models.TextField()
    
     
    def get_absolute_urls(self): 
        return reverse(
            "book:detail", 
            kwargs={ 'pk': self.pk} 
        )

    def __str__(self):
        return self.BookName


class DevoteRecord(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Book = models.ForeignKey(Book,on_delete=models.CASCADE)
    DevoteTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.User.username + '捐献了' + self.Book.BookName
    





class BorrowRecord(models.Model):
    Borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    BookBorrowed = models.ForeignKey(Book, null = True, on_delete = models.CASCADE)
    BeginTime = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default = False)
    def __str__(self):
        return self.Borrower.username + "借了" + self.BookBorrowed.BookName

