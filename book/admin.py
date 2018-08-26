from django.contrib import admin
from .models import *

admin.site.register(Book)
admin.site.register(BorrowRecord)
admin.site.register(DevoteRecord)
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ['borrow_date', 'begin_time', 'end_time']
