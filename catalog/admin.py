from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

"""
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(Language)
"""
"""
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Language, LanguageAdmin)
"""
# Define the admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status','borrower', 'due_back', 'id')

    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

class AuthorInline(admin.TabularInline):
    model = Author

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    #readonly_fields = ('author',)

    inlines = [BooksInstanceInline]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass



# Register the admin class with the associated model
