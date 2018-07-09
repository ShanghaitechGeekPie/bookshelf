from . import views
from django.urls import path,include

app_name = "book"

urlpatterns = [
    path('', views.IndexView.as_view(),name = 'homepage'),
    path('<int:book_id>',views.detail,name = 'detail'),
    path('book/add',views.BookCreate.as_view(),name = "book-add"),
]
