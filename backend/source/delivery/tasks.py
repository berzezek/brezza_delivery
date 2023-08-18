from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from celery import shared_task
from delivery.utils import create_today_orders, delivered_time_to_deadline


def create_my_task():
    # Удаляем все интервалы и задачи, которые были созданы ранее
    IntervalSchedule.objects.all().delete()
    PeriodicTask.objects.all().delete()

    # Создаем или получаем интервал в один час
    interval_one_hour, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.HOURS,
    )

    crontab_every_night, _ = CrontabSchedule.objects.get_or_create(
        minute=59,
        hour=23,
    )

    crontab_every_evening, _ = CrontabSchedule.objects.get_or_create(
        minute=0,
        hour=20,
    )


    # Создаем или получаем задачу, которая будет выполняться каждый час
    PeriodicTask.objects.get_or_create(
        interval=interval_one_hour,
        name=f"Создание заказов по расписанию",  # Уникальное имя для этой задачи
        task="delivery.tasks.create_dayly_orders",  # Имя вашей celery задачи, которую нужно запустить
    )

    # Создаем или получаем задачу, которая будет выполняться в 23:59
    PeriodicTask.objects.get_or_create(
        crontab=crontab_every_night,
        name=f"Закрытие всех необработанных заказов",  # Уникальное имя для этой задачи
        task='delivery.tasks.set_delivered_time_to_deadline',  # Имя вашей celery задачи, которую нужно запустить
    )

    # Создаем или получаем задачу, которая будет выполняться в 20:00
    PeriodicTask.objects.get_or_create(
        crontab=crontab_every_evening,
        name=f"Отправка отчета админу",  # Уникальное имя для этой задачи
        task='delivery.tasks.send_report_to_admin',  # Имя вашей celery задачи, которую нужно запустить
    )

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
    
@shared_task
def send_report_to_admin():
    print('Запущена задача отправки отчета админу')
    pass