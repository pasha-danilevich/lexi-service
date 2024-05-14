from apps.user.models import UserBookRelation, User
from apps.book.models import Book
from apps.word.models import UserWord, Word

from config.settings import p, print_local_var
from django.test import TestCase


user = User.objects.get(id=1)
levels_length = user.settings.get('levels').__len__()
user_word = UserWord.objects.filter(user_id = user.id)
word = Word.objects.get(text='hello')

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

def create_users(count):
    for i in range(count):
        user = User.objects.create(
            username='example_user' + f'{i}',
            email='example@example.com' + f'{i}',
            password='strongpassword',
            is_active=True,
            activated_email=True,
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
    def test_is_related_user(self):
        create_users(4)
        
        # uw = user_word.word_related_with_user.all()
        wu = word.user_related_with_word.all()
        
        print_local_var(locals=locals())
        # word = 

        
        # p(UserBookRelation.objects.all())

        


