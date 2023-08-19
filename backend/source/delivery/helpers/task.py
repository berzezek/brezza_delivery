from delivery.models import Order, DeliverySchedule, Schedule
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Prefetch, F


def create_today_orders():
    '''
    Создание заказов на сегодня.
        Каждый 10 минут проверяет, есть ли у заказчиков расписание и если есть, то создает заказ на сегодня, 
        при условии что текущее время находится в промежутке между временем доставки и временем доставки минус 1 час 10 минут.
        т.е. если у заказчика есть расписание на сегодня в 10:00, то заказ будет создан с 8:50 до 10:00.

        Мы проходим списком по DeliverySchedule и смотрим все связанные с ними Schedule.
        Находим Schedule, у которых day_of_week совпадает с сегодняшним днем недели и время доставки в промежутке между временем доставки и временем доставки минус 1 час 10 минут.
        Создаем заказ с учетом временной зоны.
    '''
    today = timezone.localtime(timezone.now()).date()
    current_local_time = timezone.localtime(timezone.now()).time()

    # Предварительно выбираем все связанные расписания с учетом дня недели
    schedules_query = Schedule.objects.filter(day_of_week=today.weekday())
    delivery_schedules = DeliverySchedule.objects.prefetch_related(
        Prefetch('delivery_schedule', queryset=schedules_query))

    for ds in delivery_schedules:
        for schedule in ds.delivery_schedule.all():
            dt = timezone.localtime(timezone.make_aware(
                datetime.combine(today, schedule.schedule_time)))
            # Время, которое будет использоваться для сравнения
            time_threshold = dt - timedelta(hours=1, minutes=10)
            if time_threshold.time() <= current_local_time <= schedule.schedule_time:
                naive_deadline = datetime.combine(
                    today, schedule.schedule_time)
                aware_deadline = timezone.make_aware(naive_deadline)
                _, created = Order.objects.get_or_create(
                    customer=ds.customer,
                    dead_line=aware_deadline
                )
                if created:
                    print(
                        f'Создан заказ для {ds.customer.title} '
                        f'на {aware_deadline}')
                else:
                    print(f'Заказ для {ds.customer.title} уже существует')


def delivered_time_to_deadline():
    '''
    Функция закрывает все незакрытые заказы.
        Вызывается каждый день в 23:59.
        Существует для того, чтобы закрыть все заказы, которые забыли или не получилось закрыть вручную.
        Назначает время доставки равным времени срока заказа.
    '''
    try:
        # Выбор всех объектов Order, у которых delivered_time = None
        orders_to_update = Order.objects.filter(delivered_time__isnull=True)

        # Обновление всех выбранных объектов Order в одном запросе
        orders_to_update.update(delivered_time=F('dead_line'))

    except Exception as e:
        print(e)



def create_my_task():
    # Удаляем все интервалы и задачи, которые были созданы ранее
    IntervalSchedule.objects.all().delete()
    PeriodicTask.objects.all().delete()

    # Создаем или получаем интервал в один час
    interval_ten_minutes, _ = IntervalSchedule.objects.get_or_create(
        every=10,
        name="Каждые 10 минут",
        period=IntervalSchedule.MINUTES,
    )

    crontab_every_night, _ = CrontabSchedule.objects.get_or_create(
        minute=59,
        hour=23,
        name="Каждый день в 23:59",
    )

    crontab_every_evening, _ = CrontabSchedule.objects.get_or_create(
        minute=0,
        hour=20,
        name="Каждый день в 20:00",
    )

    # Создаем или получаем задачу, которая будет выполняться каждый час
    PeriodicTask.objects.get_or_create(
        interval=interval_ten_minutes,
        name=f"Создание заказов по расписанию",  # Уникальное имя для этой задачи
        # Имя вашей celery задачи, которую нужно запустить
        task="delivery.tasks.create_dayly_orders",
    )

    # Создаем или получаем задачу, которая будет выполняться в 23:59
    PeriodicTask.objects.get_or_create(
        crontab=crontab_every_night,
        name=f"Закрытие всех необработанных заказов",  # Уникальное имя для этой задачи
        # Имя вашей celery задачи, которую нужно запустить
        task='delivery.tasks.set_delivered_time_to_deadline',
    )

    # Создаем или получаем задачу, которая будет выполняться в 20:00
    PeriodicTask.objects.get_or_create(
        crontab=crontab_every_evening,
        name=f"Отправка отчета админу",  # Уникальное имя для этой задачи
        # Имя вашей celery задачи, которую нужно запустить
        task='delivery.tasks.send_report_to_admin',
    )
