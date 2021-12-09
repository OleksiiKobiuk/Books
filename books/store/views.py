import django_filters.rest_framework
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import render

from .serializer import BooksSerializer
from .models import Book
from .permissions import IsOwnerOrStaffOrReadOnly


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    # Додаємо фільтер
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # permission_classes = [IsAuthenticated] # тільки авторизовані користувачі зможуть переглядати список книг
    permission_classes = [IsOwnerOrStaffOrReadOnly] #переглядати список зможуть всі користувачі, в т.ч. незалогінені
    filter_fields = ['price'] #визначаємо поля фільтру, по яким будемо фільтрувати
    search_fields = ['name', 'author_name'] # пошук має відбуватися в двох і більше полях, бо для одного поля достатньо фільтра
    ordering_fields = ['price', 'author_name']

    # Перевизанчаємо метод def perform_create із ModelViewSet -> CreateModelMixin,
    # присвоюючи користувача тій книзі, яку він створив
    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user    # validated_data - дані із serializer після того як він пройщов валідацію
        # так як create може робити лише авторизований користувач, то self.request.user буде завжди
        serializer.save()

def auth(request):
    return render(request, 'oauth.html')
