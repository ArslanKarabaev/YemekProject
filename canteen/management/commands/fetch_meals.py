import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from canteen.models import Meal
from decimal import Decimal


class Command(BaseCommand):
    help = "Парсит меню столовой с сайта Manas"

    def handle(self, *args, **kwargs):
        url = "https://beslenme.manas.edu.kg/1"

        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Ошибка подключения: {e}"))
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # Находим все контейнеры с блюдами
        gallery_rows = soup.find_all('div', class_='row mbr-gallery mt-4')

        if not gallery_rows:
            self.stdout.write(self.style.ERROR("Не найдены ряды с блюдами!"))
            return

        # Очистка базы
        try:
            Meal.objects.all().delete()
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Не удалось очистить таблицу: {e}"))

        count = 0
        for gallery_row in gallery_rows:
            # Находим все карточки блюд в текущем ряду
            meal_cards = gallery_row.find_all('div', class_='col-12 col-md-6 col-lg-3 item gallery-image')

            for card in meal_cards:
                try:
                    # Название блюда
                    name = card.find('h5', class_='item-title').text.strip()

                    # Цена
                    price_text = card.find('h6', class_='text-muted').text.strip()
                    price = Decimal(''.join(c for c in price_text if c.isdigit() or c == '.'))

                    # Изображение
                    img_tag = card.find('img', class_='w-100')
                    image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ''

                    # Корректировка URL изображения
                    if image_url and not image_url.startswith(('http', '//')):
                        image_url = f'https://beslenme.manas.edu.kg{image_url}'

                    Meal.objects.create(
                        name=name,
                        price=price,
                        image_url=image_url
                    )
                    count += 1
                    self.stdout.write(self.style.SUCCESS(f"Добавлено: {name} - {price} сом"))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Ошибка при обработке карточки: {e}"))
                    continue

        self.stdout.write(self.style.SUCCESS(f"Успешно добавлено {count} блюд"))