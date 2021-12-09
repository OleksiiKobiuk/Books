from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Book
from store.serializer import BooksSerializer


class BookSerializerTestCase(TestCase): #owner = 1, щоб пройти тест
    def test_ok(self):
        # self.user = User.objects.create(username='test_username')
        book_1 = Book.objects.create(name='Test book 1', price=120.3, author_name='Author 1')
        book_2 = Book.objects.create(name='Test book 2', price=320.3, author_name='Author 2')
        data = BooksSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '120.30', # ставимо з двома знаками після коми, бо в моделі 'price' -
                'author_name': 'Author 1',
                'owner': None
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '320.30',
                'author_name': 'Author 2',
                'owner': None
            },
        ]

        self.assertEqual(expected_data, data)
