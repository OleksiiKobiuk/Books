import django_filters.rest_framework
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import render

from .serializer import BooksSerializer
from .models import Book


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    # Додаємо фільтер
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # permission_classes = [IsAuthenticated] # тільки авторизовані користувачі зможуть переглядати список книг
    permission_classes = [IsAuthenticatedOrReadOnly] #переглядати список зможуть всі користувачі, в т.ч. незалогінені
    filter_fields = ['price'] #визначаємо поля фільтру, по яким будемо фільтрувати
    search_fields = ['name', 'author_name'] # пошук має відбуватися в двох і більше полях, бо для одного поля достатньо фільтра
    ordering_fields = ['price', 'author_name']

def auth(request):
    return render(request, 'oauth.html')