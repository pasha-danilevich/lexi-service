from apps.user.models import UserBookRelation, User
from apps.book.models import Book

from config.settings import p
from django.test import TestCase

def create_books(count, user):
    for i in range(count):
        book = Book.objects.create(
            title=f'Example Book №{i+1}',
            author='John Doe',
            page_count=300,
            slug='example-book',
            author_upload=user,
            book='text'  
        )
        
class TestStringMethods(TestCase):

    def test_create_and_update(self):
        user = User.objects.create(
            username='example_user',
            email='example@example.com',
            password='strongpassword',
            is_active=True,
            activated_email=True,
        )
        create_books(5, user=user)
        
        u = User.objects.get(id=1)
        b = Book.objects.get(id=1)
        b2 = Book.objects.get(id=2)
        
        obj, created = UserBookRelation.objects.update_or_create(
            user=u, 
            book=b, 
            defaults={
                "target_page": 10
                }
        )
        obj, created = UserBookRelation.objects.update_or_create(
            user=u, 
            book=b, 
            defaults={
                "target_page": 30
                }
        )
        obj, created = UserBookRelation.objects.update_or_create(
            user=u, 
            book=b2, 
            defaults={
                "target_page": 30
                }
        )
        obj, created = UserBookRelation.objects.update_or_create(
            user=u, 
            book=b2, 
            defaults={
                "target_page": 102
                }
        )
        obj, created = UserBookRelation.objects.update_or_create(
            user=u, 
            book=b2, 
            defaults={
                "target_page": 145
                }
        )


        
        p(UserBookRelation.objects.all())



