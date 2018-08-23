from django.shortcuts import render , HttpResponseRedirect
from django.views import generic
from .models import Book,BorrowRecord
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from .form import UserForm, BorrowRecordForm,BookForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q

import urllib.request 
from PIL import Image


# Create your views here.
 
all_book = Book.objects.all()


def index(request):
    if not request.user.is_authenticated:
        books = Book.objects.all()
        return HttpResponseRedirect('/book/login')
    else:
        books = Book.objects.all()
        query = request.GET.get("q")
        if query:
            books = books.filter(
                Q(BookName__icontains=query) |
                Q(Author__icontains=query) |
                Q(Publisher__icontains=query)
            ).distinct()
            books.filter(~Q(Quantity = 0))
            return render(request, 'book/homepage.html', {
                'books': books,
            })
        else:
            books = Book.objects.filter(~Q(Quantity = 0))
            return render(request, 'book/homepage.html', {'books': books})

def logout_user(request):
    if not request.user.is_authenticated:
        return render(request, 'book/login.html', {'error_message' :'您还没有登录'})
    else:
        logout(request)
        return HttpResponseRedirect('/book')

def login_user(request):
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
            return HttpResponseRedirect('/book')
        else :
            return render(request, 'book/login_u.html',{'error_message' : "您还没有注册"} )
    else:
        # if status != 0:
        #     return render(request,'book.login.html',{'error_message':'请先登录'})
        return render(request, 'book/login_u.html')




# def Detail(request,book_id):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect('book/login')
#     else:
#         book = get_object_or_404(Book, pk=book_id)
#         context = {
#             'book' : book,
#         }
#         return render(request,'book/item.html',context)
    


def create_book(request):
    if not request.user.is_authenticated: 
        return HttpResponseRedirect('book/login')
    else:
        form = BookForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            book = form.save(commit=False)
            thisISBN = book.ISBN
            existingISBN = Book.objects.filter(ISBN = thisISBN)
            existingBookName = Book.objects.filter(BookName = book.BookName)
            if existingISBN.count() > 0:
                existingbook = existingISBN[0]
                existingbook.Quantity += 1
                existingbook.save()
                return HttpResponseRedirect('/book')
            if existingBookName.count() > 0:
                existingbook = existingBookName[0]
                existingbook.Quantity += 1
                existingbook.save()
                return HttpResponseRedirect('/book')
            # save the image front internet
            url = book.FrontPage
            data = urllib.request.urlretrieve(url)
            frontpage = Image.open(data[0])
            new_route = './book/static/' + str(book.id) + '_frontpage.jpg'
            frontpage.save(new_route,'JPEG')
            book.FrontPage = str(book.id) + '_frontpage.jpg'
            book.save()
            return HttpResponseRedirect('/book')
        context = {
            "form": form,
            "all_user" : User.objects.all(),
        }
        return render(request, 'book/add_book.html', context)




def BorrowBook(request, book_id):
    if not request.user.is_authenticated:
        return render(request , 'book/login.html' ,{ 'error_message' : " 请先登录"} )
    else:    

        borrowRecords = BorrowRecord.objects.filter( Borrower = request.user ).filter(finished = False)
        if borrowRecords.count() > 4:
            return HttpResponseRedirect('/book')
        borrowed_books = set()
        for record in borrowRecords:
            borrowed_books.add(record.BookBorrowed.pk)
        if book_id in borrowed_books:
            context = {
                'books':Book.objects.all(),
                'error_message': "您已经借过这本书了",
            }
            return HttpResponseRedirect('/book')
        
        user = request.user
        book = Book.objects.get(pk=book_id)
        record = BorrowRecord(Borrower=request.user,BookBorrowed = book)
        if book.Quantity >= 1:
            book.Quantity -= 1
            book.save()
            record.save() 
            return HttpResponseRedirect("/book/%d/profile" % user.id)
        else:
            return Http404


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
            return HttpResponseRedirect('/book/%d/profile' % request.user.id)
        else:
            print('success')
            thisRecord = BorrowRecord.objects.filter(Borrower = request.user , BookBorrowed = Book.objects.get(id = book_id)).filter(finished = False)
            thisRecord = thisRecord[0]
            source = Book.objects.get(id = thisRecord.BookBorrowed.id)
            source.Quantity += 1
            source.save()
            
            thisRecord.finished = True
            thisRecord.save()

            return HttpResponseRedirect('/book/%d/profile' % request.user.id)


def userProfile(request,user_id):
    user = request.user
    if not user.is_authenticated:
        return render(request, 'book/login.html' ,{ error_message : "Please login first"} )
    else:

        borrowRecords = BorrowRecord.objects.filter( Borrower = request.user ).filter(finished = False)

        borrowed_books = set()

        for record in borrowRecords:
            borrowed_books.add(record.BookBorrowed.pk)

        borrowed_books = Book.objects.filter(pk__in = borrowed_books)

        return render(request , 'book/userprofile.html' , {'books': borrowed_books})
        


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

