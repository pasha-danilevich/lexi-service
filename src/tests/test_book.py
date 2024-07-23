from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.book.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()


class BookBookmarkSetUp(APITestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.generate_count = 10

    def generate_book_data(self) -> list[dict]:
        book_data_list = []

        for i in range(self.generate_count):
            book_data = {
                'title': f'Test Book {i}',
                'author': f'Test Author {i}',
                'book': f"\nGerald Murnane\n\n\nA Million Windows\n\n\n\nAbout {i}"
            }
            book_data_list.append(book_data)

        return book_data_list

    def create_and_authenticate_user(self):
        """Создание и аутентификация пользователя."""
        user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.force_authenticate(user=user)  # type: ignore

    def create_books(self):
        """Создание книг на основе данных из book_data_list."""

        for book_data in self.book_data_list:
            response = self.client.post(
                reverse('book-list-create'), book_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def create_bookmarks(self):
        books_queryset = Book.objects.all()[:3]

        for book in books_queryset:
            data = {
                "book_id": book.pk,
                "target_page": 1
            }
            response = self.client.post(
                reverse('bookmark-list-create'), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        self.create_and_authenticate_user()

        self.book_data_list = self.generate_book_data()

        self.create_books()


class BookListCreateTestCase(BookBookmarkSetUp):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.url = reverse('book-list-create')

    def test_create_books(self):
        """
        Проверка созданных книг
        """

        self.assertEqual(Book.objects.all().count(), self.generate_count)

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
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            pass

    def test_list_books(self):
        """
        Проверка получения списка книг
        """
        response = self.client.get(self.url)
        title = self.book_data_list[0].get('title')
        data = response.data['results']  # type: ignore

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 10)


class BookmarkListCreateTestCase(BookBookmarkSetUp):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.url = reverse('bookmark-list-create')

    def test_bookmark_list(self):
        """
        Проверка получения списка закладок
        """
        print(Book.objects.all().count(), 'test_bookmark_list')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
