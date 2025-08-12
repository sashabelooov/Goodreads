from django.shortcuts import render
from django.views import View
from .models import Book
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator


# class BookListView(ListView):
#     template_name = "books/list.html"
#     queryset = Book.objects.all()
#     context_object_name = "books"
#     paginate_by = 2


class BookListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)
        page_number = request.GET.get('page',1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'books/list.html', {"page_obj":page_obj})



class BookDetailView(DetailView):
    template_name = "books/detail.html"
    pk_url_kwarg = 'id'
    model = Book

# class BookDetailView(View):
#     def get(self, request, id):
#         book = Book.objects.get(id=id)
#         return render(request, "books/detail.html", {"book":book})