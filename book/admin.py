from django.contrib import admin
from .models import Book,BorrowRecord

admin.site.register(Book)
admin.site.register(BorrowRecord)
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ['borrow_date', 'begin_time', 'end_time']
