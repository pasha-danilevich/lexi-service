import django
from django.core.management.base import BaseCommand
from django.apps import AppConfig, apps
from django.db import connection


django.setup()

class Command(BaseCommand):
    help = 'Информация о базе данных'

    def add_arguments(self, parser):
        parser.add_argument('--app_name', type=str)

    def handle(self, *args, **options):
        app_name: str = options.get('app_name')
        
        if app_name:
            app_configs = apps.get_app_config(app_name)
        else:
            app_configs = apps.get_app_configs()
            app_configs = [
                app_config
                for app_config in app_configs
                if not app_config.name.startswith('django.')
            ]
            
        for app in app_configs:
            app: AppConfig
            app_name = app.name.split('.')[-1]
            models = app.get_models(include_auto_created=True)
            
            for model in models:
                self.print_model_info(app_name=app_name, model=model)
            
    def print_model_info(self, app_name: str, model):
        model_name = model.__name__
        count = model.objects.count()
        self.stdout.write(f"Модель: {model_name}")
        self.stdout.write(f"Количество записей: {count}")
        self.get_model_weight('public', f'{app_name}_{model_name.lower()}')
        self.stdout.write("---------")    
            
    def get_model_weight(self, schemaname: str, relname: str):
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT
                  "schemaname",
                  "relname",
                  pg_size_pretty(pg_relation_size(quote_ident("schemaname") || '.' || quote_ident("relname"))) AS size
                FROM
                  pg_stat_user_tables
                WHERE "schemaname" = '{schemaname}' AND "relname" = '{relname}'
                ORDER BY
                  pg_relation_size(quote_ident("schemaname") || '.' || quote_ident("relname")) DESC
            """)
            row = cursor.fetchone()

            if row:
                _, _, size = row
                self.stdout.write(f"Размер: {size}")
            else:
                self.stdout.write(f"Таблица {relname} не найдена")