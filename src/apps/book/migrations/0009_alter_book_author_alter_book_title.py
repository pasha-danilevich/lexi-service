# Generated by Django 5.0.4 on 2024-08-09 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_rename_userbook_bookmark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(blank=True, max_length=50, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=50, verbose_name='title'),
        ),
    ]