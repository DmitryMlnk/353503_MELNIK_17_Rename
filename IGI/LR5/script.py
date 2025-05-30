import logging
from django.contrib.auth.models import User
from main.models import Client, News
from django.utils import timezone

logger = logging.getLogger(__name__)

def populate_data():
    try:
        # Настройка администратора
        logger.debug("Проверка наличия администратора")
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_superuser': True,
                'is_staff': True,
                'is_active': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            logger.info("Создан администратор: admin")
        else:
            logger.info("Администратор уже существует")

        # Создание клиента для администратора
        if not hasattr(admin, 'client'):
            Client.objects.create(
                user=admin,
                phone_number='+375(29)999-99-99',
                address='Минск, ул. Админская, 1',
                role='admin',
                age=30
            )
            logger.info("Создан клиент для администратора")

        # Создание тестового пользователя (например, Dmitry)
        logger.debug("Проверка наличия пользователя Dmitry")
        dmitry, created = User.objects.get_or_create(
            username='Dmitry',
            defaults={
                'email': 'dmitry@example.com',
                'is_active': True
            }
        )
        if created:
            dmitry.set_password('Dmitry_123')
            dmitry.save()
            logger.info("Создан пользователь: Dmitry")
        else:
            logger.info("Пользователь Dmitry уже существует")

        # Создание клиента для Dmitry
        if not hasattr(dmitry, 'client'):
            Client.objects.create(
                user=dmitry,
                phone_number='+375(29)123-45-67',
                address='Минск, ул. Тестовая, 10',
                role='customer',
                age=25
            )
            logger.info("Создан клиент для Dmitry")

        # Создание новостей
        logger.debug("Проверка наличия новостей")
        if not News.objects.exists():
            news_data = [
                {
                    'title': 'Открытие нового филиала',
                    'summary': 'Мы рады объявить об открытии нового филиала в Минске!',
                    'content': 'Наш новый филиал в Минске начнет работу с 1 июня 2025 года. Приглашаем всех на открытие!',
                    'pub_date': timezone.now(),
                    'author': admin
                },
                {
                    'title': 'Скидки на летнее обслуживание',
                    'summary': 'Получите скидку 20% на все услуги в июне!',
                    'content': 'Весь июнь 2025 года действуют скидки 20% на все услуги, включая замену масла и диагностику.',
                    'pub_date': timezone.now(),
                    'author': admin
                }
            ]
            for news_item in news_data:
                News.objects.create(**news_item)
                logger.info(f"Создана новость: {news_item['title']}")
        else:
            logger.info("Новости уже существуют в базе данных")

    except Exception as e:
        logger.error(f"Ошибка при создании тестовых данных: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("Запуск скрипта populate_data.py")
    populate_data()
    logger.info("Скрипт populate_data.py завершен")