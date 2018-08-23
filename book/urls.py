from . import views
from django.urls import path,include

app_name = "book"

urlpatterns = [
    path('', views.index, name = 'homepage'),
    path('add',views.create_book,name = "book-add"),
    path('register',views.register,name = 'register'),
    path('login',views.login_user, name = 'login'),
    path('logout',views.logout_user, name = 'logout'),
    path('<int:book_id>/borrow',views.BorrowBook ,name = 'borrow'),
    path('<int:book_id>/return', views.returnBook, name = 'return'),
    path('<int:user_id>/profile',views.userProfile, name = 'profile')
]
 