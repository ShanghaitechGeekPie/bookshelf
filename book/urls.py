from . import views
from django.urls import path,include

app_name = "book"

urlpatterns = [
    path('', views.index, name = 'homepage'),
    path('<int:book_id>/detail',views.DetailView.as_view(),name = 'detail'),
    path('book/add',views.create_book,name = "book-add"),
    path('register',views.register,name = 'register'),
    path('loginf',views.login_fuck, name = 'login'),
    path('logout',views.logout, name = 'logout'),
    path('<int:book_id>/borrow',views.BorrowBook ,name = 'borrow'),
    path('<int:book_id>/return', views.returnBook, name = 'return'),
    path('<int:user_id>/profile',views.userProfile, name = 'profile')
]
 