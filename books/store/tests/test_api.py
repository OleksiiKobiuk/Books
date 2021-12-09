# тестування API запитів
import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from store.models import Book
from store.serializer import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):  # дана функція буде запускатися перед кожним тестом
        self.user = User.objects.create(username='test_username')  # створення користувача
        self.book_1 = Book.objects.create(name='Test book 1', price=100, author_name='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price='400', author_name='Author 2', owner=self.user)
        self.book_3 = Book.objects.create(name='Test book 3 Author 1', price='320.3', author_name='Author 3',
                                          owner=self.user)

    def test_get(self):
        url = reverse('book-list')
        # print(url)
        response = self.client.get(url)

        # перевіряємо серіалізовані дані тестових book_1 і book_2, щоб у випадку зміни самого серіалізатора BooksSerializer
        # тест не впав, оскільки виходить, що серіалізатор зрівнюється сам із собою
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        # print(response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 400})
        serializer_data = BooksSerializer([self.book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        serializer_data = BooksSerializer([self.book_1, self.book_3, self.book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            "name": "ddddd",
            "price": 12,
            "author_name": "DC"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)  # логінація юзера
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))  # 'book-detail' - створює url, який має ID
        data = {
            "name": self.book_1.name,
            "price": 456,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)  # логінація юзера
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()  # Використовується в основному при тестах, коли слід одразу витягти з БД попередньо змінений об'єкт.
        self.assertEqual(456, self.book_1.price)

    def test_del(self):
        url = reverse('book-detail', args=(self.book_2.id,))  # 'book-detail' - створює url, який має ID
        self.client.force_login(self.user)  # логінація юзера
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        # self.book_2.refresh_from_db() # Використовується в основному при тестах, коли слід одразу витягти з БД попередньо змінений об'єкт.
        self.assertEqual(2, Book.objects.all().count())

    def test_get_by_id(self):
        url = reverse('book-detail', args=(self.book_3.id,))  # 'book-detail' - створює url, який має ID
        self.client.force_login(self.user)  # логінація юзера
        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('320.3', self.book_3.price)
        self.assertEqual('Test book 3 Author 1', self.book_3.name)

    def test_update_not_owner(self):  #тест, що не власник об'єкту не зможе його змінити
        self.user2 = User.objects.create(username='test_username2')
        url = reverse('book-detail', args=(self.book_1.id,))  # 'book-detail' - створює url, який має ID
        data = {
            "name": self.book_1.name,
            "price": 456,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)  # логінація юзера
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.book_1.refresh_from_db()  # Використовується в основному при тестах, коли слід одразу витягти з БД попередньо змінений об'єкт.
        self.assertEqual(100, self.book_1.price)

    def test_update_not_owner_but_staff(self):  #тест, що не власник об'єкту не зможе його змінити, але staff зможе
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('book-detail', args=(self.book_1.id,))  # 'book-detail' - створює url, який має ID
        data = {
            "name": self.book_1.name,
            "price": 456,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)  # логінація юзера
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()  # Використовується в основному при тестах, коли слід одразу витягти з БД попередньо змінений об'єкт.
        self.assertEqual(456, self.book_1.price)
