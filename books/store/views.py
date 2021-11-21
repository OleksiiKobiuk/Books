import django_filters.rest_framework
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializer import BooksSerializer
from .models import Book


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    # Додаємо фільтер
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['price'] #визначаємо поля фільтру, по яким будемо фільтрувати
    search_fields = ['name', 'author_name'] # пошук має відбуватися в двох і більше полях, бо для одного поля достатньо фільтра
    ordering_fields = ['price', 'author_name']