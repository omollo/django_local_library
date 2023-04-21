from django.shortcuts import render

from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required



def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_language = Language.objects.count()
    book_contains = Book.objects.filter(title__icontains="ove")

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_language': num_language,
        'book_contains':book_contains,
        'num_visits': num_visits,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)

class BookDetailView(generic.DetailView):
    model = Book
    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)

       # return render(request, 'catalog/books/book_detail.html', context={'book': book})
    template_name = 'catalog/books/book_detail.html'  # Specify your own template name/location

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # your own name for the list as a template variable
    paginate_by = 2

    def get_queryset(self):
       # return Book.objects.filter(title__icontains='lovsds')[:5] # Get 5 books
        return Book.objects.all()
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data by omodroid'
        return context
    template_name = 'catalog/books/book_list.html'  # Specify your own template name/location

class AuthorDetailView(generic.DetailView):
    model = Author
    def author_detail_view(request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)

       # return render(request, 'catalog/books/book_detail.html', context={'book': book})
    template_name = 'catalog/books/author_detail.html'  # Specify your own template name/location


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'   # your own name for the list as a template variable
    paginate_by = 3

    def get_queryset(self):
       # return Book.objects.filter(title__icontains='lovsds')[:5] # Get 5 books
        return Author.objects.all()
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data by omodroid'
        return context
    template_name = 'catalog/books/author_list.html'  # Specify your own template name/location



class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    paginate_by = 3

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    template_name = 'catalog/books/bookinstance_list_borrowed_user.html'


class AllBorrowedListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/books/all_borrowed.html'

    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')



import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/books/book_renew_librarian.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    template_name = 'catalog/books/author_form.html'


class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    template_name = 'catalog/books/author_form.html'


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'catalog/books/author_confirm_delete.html'



from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Book

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'summary', 'isbn']
    initial = {'isbn': '1234567890'}
    template_name = 'catalog/books/book_form.html'


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    template_name = 'catalog/books/book_form.html'


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    template_name = 'catalog/books/book_confirm_delete.html'
