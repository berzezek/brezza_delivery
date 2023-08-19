from celery import shared_task
from delivery.helpers.task import create_today_orders, delivered_time_to_deadline


# Создаем заказы по расписанию
@shared_task
def create_dayly_orders():
    print('Запущена задача создания заказов')
    create_today_orders()

# Закрываем заказы по расписанию в 23:59


@shared_task
def set_delivered_time_to_deadline():
    print('Запущена задача закрытия необработанных заказов')
    delivered_time_to_deadline()

# Отправка отчета админу в 20:00


@shared_task
def send_report_to_admin():
    print('Запущена задача отправки отчета админу')
    pass
