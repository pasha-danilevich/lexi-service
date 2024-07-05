# Generated by Django 5.0.4 on 2024-06-29 09:51

import apps.user.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_book_book'),
        ('user', '0005_userbookrelation_target_page_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activated_email',
            field=models.BooleanField(default=False, verbose_name='activated_email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='userbookrelation',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_users', to='book.book'),
        ),
        migrations.AlterField(
            model_name='userbookrelation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('levels', models.JSONField(default=apps.user.models.levels_default)),
                ('dark_theme', models.BooleanField(default=False)),
                ('count_word_in_round', models.IntegerField(default=10)),
                ('number_of_false_set', models.IntegerField(default=3)),
                ('time_to_view_result', models.IntegerField(default=1000)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]