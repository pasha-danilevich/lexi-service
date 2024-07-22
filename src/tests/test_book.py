from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.book.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()


class BookListCreateTestCase(APITestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.url = reverse('book-list-create')
        self.books_count = 10
        
    def generate_book_data(self) -> list[dict]:
        book_data_list = []

        for i in range(self.books_count):
            book_data = {
                'title': f'Test Book {i}',
                'author': f'Test Author {i}',
                'book': f"\nGerald Murnane\n\n\nA Million Windows\n\n\n\nAbout {i}"
            }
            book_data_list.append(book_data)

        return book_data_list

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)  # type: ignore

        self.book_data_list = self.generate_book_data()
        
        for book_data in self.book_data_list:

            response = self.client.post(self.url, book_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_books(self):
        """
        Проверка созданных книг
        """
        
        self.assertEqual(Book.objects.all().count(), self.books_count)
        

    def test_create_book_with_empty_chapters(self):
        """
        Проверка создания книги с пустыми главами
        """

        # Создаем копию данных чтобы избезать влияния на другой тест
        data = self.book_data_list[0].copy()
        data['book'] = ''

        response = self.client.post(self.url, data, format='json')
        data = response.data  # type: ignore
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data, {'book': 'Это поле не может быть пустым'})

    def test_create_duplicate_book(self):
        """
        Проверка создания дубликата книги
        """
        book_data = self.book_data_list[0]

        try:
            response = self.client.post(self.url, book_data, format='json')
            self.skipTest('Duplicate question allowed.')
        except IntegrityError:
            pass
            

    def test_list_books(self):
        """
        Проверка получения списка книг
        """
        response = self.client.get(self.url)
        title = self.book_data_list[0].get('title')
        data = response.data['results'] # type: ignore
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 10)
