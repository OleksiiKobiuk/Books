from rest_framework.viewsets import ModelViewSet

from .serializer import BooksSerializer
from .models import Book


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
