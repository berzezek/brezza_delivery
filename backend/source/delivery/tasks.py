from delivery.models import Order, DeliverySchedule
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery import shared_task
from django.utils import timezone
import datetime


def create_every_hour_task():
    # Создаем или получаем интервал в один час
    interval, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.HOURS,
    )

    # Ваша celery задача
    task_name = 'delivery.tasks.create_dayly_orders'

    # Создаем или получаем задачу, которая будет выполняться каждый час
    PeriodicTask.objects.get_or_create(
        interval=interval,
        name=f"Run {task_name} every hour",  # Уникальное имя для этой задачи
        task=task_name,  # Имя вашей celery задачи, которую нужно запустить
    )

def create_today_orders():
    today = timezone.localtime(timezone.now()).date()
    current_local_time = timezone.localtime(timezone.now()).time()

    delivery_schedules = DeliverySchedule.objects.all()
    for ds in delivery_schedules:
        if ds.delivery_shedule.exists():  # используйте `.exists()` для проверки наличия связанных объектов
            for schedule in ds.delivery_shedule.all():
                # если день совпадает с сегодняшним днем
                # и текущее время в промежутке между временем доставки и временем доставки минус 1 час 10 минут
                time_threshold = (timezone.localtime(timezone.now()) - timezone.timedelta(hours=1, minutes=10)).time()
                if schedule.day_of_week == str(today.weekday()) and time_threshold <= current_local_time <= schedule.schedule_time:
                    # создание заказа с учетом временной зоны
                    naive_deadline = datetime.datetime.combine(today, schedule.schedule_time)
                    aware_deadline = timezone.make_aware(naive_deadline)
                    order, created = Order.objects.get_or_create(
                        customer=ds.customer,
                        dead_line=aware_deadline
                    )
                    if created:
                        print(f'Создан заказ для {ds.customer.title} на {aware_deadline}')


@shared_task
def create_dayly_orders():
    print('Запущена задача создания заказов')
    create_today_orders()
