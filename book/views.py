from django.shortcuts import render , HttpResponseRedirect
from django.views import generic
from .models import Book,BorrowRecord
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from .form import UserForm, BorrowRecordForm,BookForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.db.models import Q

import urllib.request 
from PIL import Image


# Create your views here.
 
all_book = Book.objects.all()


def index(request):
    if not request.user.is_authenticated:
        print('here')
        books = Book.objects.all()
        return render(request, 'book/homepage_guest.html', {'books':all_book})
    else:
        books = Book.objects.all()
        query = request.GET.get("q")
        if query:
            books = books.filter(
                Q(BookName__icontains=query) |
                Q(Author__icontains=query) |
                Q(Publisher__icontains=query)
            ).distinct()
            return render(request, 'book/homepage.html', {
                'books': books,
            })
        else:
            books = Book.objects.all()
            print(type(books))
            return render(request, 'book/homepage.html', {'books': books})

def logout(request):
    if not request.user.is_authenticated:
        return render(request, 'book/login.html', {'error_message' :'您还没有登录'})
    else:
        return render(request, 'book/homepage_guest.html',{'books': all_book})

def login_fuck(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            books = Book.objects.all()
            context = {
                'books' : books
            }
            return render(request, 'book/homepage.html', context)
        else :
            return render(request, 'book/login.html',{'error_message' : "您还没有注册"} )
    else:
        return render(request, 'book/login.html')




def Detail(request,book_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('book/login')
    else:
        book = get_object_or_404(Book, pk=book_id)
        context = {
            'book' : book,
        }
        return render(request,'book/item.html',context)
    


def create_book(request):
    if not request.user.is_authenticated: 
        return HttpResponseRedirect('book/login')
    else:
        form = BookForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.save()
            # save the image front internet
            url = album.FrontPage
            data = urllib.request.urlretrieve(url)
            frontpage = Image.open(data[0])
            new_route = './book/static/' + str(album.id) + '_frontpage.jpg'
            frontpage.save(new_route,'JPEG')
            album.FrontPage = str(album.id) + '_frontpage.jpg'
            album.save()
            #
            return HttpResponseRedirect('/book')
        context = {
            "form": form,
        }
        return render(request, 'book/add_book.html', context)




def BorrowBook(request, book_id):
    if not request.user.is_authenticated:
        return render(request , 'book/login.html' ,{ 'error_message' : "Please login first"} )
    else:    
        user = request.user
        book = Book.objects.get(pk=book_id)
        record = BorrowRecord(Borrower=request.user,BookBorrowed = book)
        record.save() 
        # form = BorrowRecordForm(request.POST or None, request.FILES or None)
        # if form.is_valid(): 
        #     record = form.save(commit=False)
        #     record.borrower = request.user
        #     record.book = get_object_or_404(Book, pk=book_id)
        #     record.save()
        # else:
        #     print('wrong')
        return HttpResponseRedirect("/book/%d/profile" % user.id)


def returnBook(request, book_id):
    if not request.user.is_authenticated:
        return render(request , 'book/login.html' ,{ error_message : "Please login first"} )
    else:
        borrowRecords = BorrowRecord.objects.filter( Borrower = request.user)
        borrowed_books_id = set()
        for record in borrowRecords:
            borrowed_books_id.add(record.BookBorrowed.pk)
        borrowed_books = Book.objects.filter(pk__in = borrowed_books_id)
        if book_id not in borrowed_books_id:
            return render(request , 'book/userprofile.html' , {"books" : borrowed_books , 'message' : "您没有借这本书"})
        else:
            thisRecord = BorrowRecord.objects.filter(Borrower = request.user , BookBorrowed = Book.objects.get(id = book_id))
            borrowed_books_id.remove(thisRecord[0].BookBorrowed.id)
            thisRecord.delete()
            borrowed_books = Book.objects.filter(pk__in = borrowed_books_id)
            context = {
                'books' : borrowed_books,
                'message' : "还书成功"
            }
            return render(request, 'book/userprofile.html' , context )


def detail(request,book_id):
    if not request.user.is_authenticated:
        return render(request, 'book/login.hrml',{ error_message : "Please login first"} )


def userProfile(request,user_id):
    user = request.user
    if not user.is_authenticated:
        return render(request, 'book/login.html' ,{ error_message : "Please login first"} )
    else:

        borrowRecords = BorrowRecord.objects.filter( Borrower = request.user)

        borrowed_books = set()

        for record in borrowRecords:
            borrowed_books.add(record.BookBorrowed.pk)

        borrowed_books = Book.objects.filter(pk__in = borrowed_books)

        return render(request , 'book/userprofile.html' , {'books': borrowed_books , 'message': "我的书架"})
        


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # borrowed_books = Book.objects.filter(user=request.user)
                return render(request, 'book/homepage.html', {'books': Book.objects.all()})
    context = {
        "form": form,
    }
    return render(request, 'book/register.html', context)

