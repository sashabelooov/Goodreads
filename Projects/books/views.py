from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import BookReviewForm
from .models import Book, BookReview
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


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()
        return render(request, "books/detail.html", {
            "book":book,
            "review_form":review_form,
        })



# class BookDetailView(DetailView):
#     template_name = "books/detail.html"
#     pk_url_kwarg = 'id'
#     model = Book


class AddReviewView(View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment'],
            )

            return redirect(reverse('books:detail', kwargs={"id": book.id}))

        return render(request, "books/detail.html", {
            "book": book,
            "review_form": review_form,
        })

# updated