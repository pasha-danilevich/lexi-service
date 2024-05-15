# Generated by Django 5.0.4 on 2024-05-15 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0006_alter_synonym_translation_alter_translation_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='frequency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='translation',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='translation',
            name='part_of_speech',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='part_of_speech',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='transcription',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
