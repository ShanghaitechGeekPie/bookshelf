from django.shortcuts import render
from django.views import generic
from .models import Book
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.http import HttpResponse,Http404


# Create your views here.

class IndexView(generic.ListView):
    template_name = "book/homepage.html"

    def get_queryset(self):

        return Book.objects.all()


class DetailView(generic.DetailView):
    model = Book
    template_name = "book/detail.html"


class BookCreate(CreateView):
    model = Book
    fields = Book.get_all_field_names()

    