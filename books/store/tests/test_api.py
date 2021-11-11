# тестування API запитів

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializer import BooksSerializer


class BooksApiTestCase(APITestCase):
    def test_get(self):
        book_1 = Book.objects.create(name='Test book 1', price='120.3')
        book_2 = Book.objects.create(name='Test book 2', price='320.3')
        url = reverse('book-list')
        # print(url)
        response = self.client.get(url)

        # перевіряємо серіалізовані дані тестових book_1 і book_2, щоб у випадку зміни самого серіалізатора BooksSerializer
        # тест не впав, оскільки виходить, що серіалізатор зрівнюється сам із собою
        serializer_data = BooksSerializer([book_1, book_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        # print(response.data)
