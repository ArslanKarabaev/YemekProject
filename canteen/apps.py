import threading
import time
from django.apps import AppConfig
from django.core.management import call_command


class CanteenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'canteen'

    def ready(self):
        def run_parser():
            while True:
                try:
                    print("Запуск ежедневного парсинга меню...")
                    call_command('fetch_meals')  # Это та самая management-команда
                    print("Парсинг завершен.")
                except Exception as e:
                    print(f"Ошибка при парсинге: {e}")
                time.sleep(86400)  # 24 часа в секундах

        if not hasattr(self, '_parser_thread_started'):
            self._parser_thread_started = True
            threading.Thread(target=run_parser, daemon=True).start()
