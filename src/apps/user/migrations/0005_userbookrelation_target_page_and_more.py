# Generated by Django 5.0.4 on 2024-04-13 09:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
        ('user', '0004_userbookrelation_delete_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbookrelation',
            name='target_page',
            field=models.IntegerField(default=1, verbose_name='target page'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userbookrelation',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_related_with_book', to='book.book'),
        ),
        migrations.AlterField(
            model_name='userbookrelation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_related_with_user', to=settings.AUTH_USER_MODEL),
        ),
    ]