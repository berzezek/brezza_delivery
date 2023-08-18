from delivery.models import Order, DeliverySchedule
from django.utils import timezone
from datetime import timedelta, datetime

def delivered_time_to_deadline():
    # Выбор всех объектов Order, у которых delivered_time = None
    orders_to_update = Order.objects.filter(delivered_time__isnull=True)

    for order in orders_to_update:
        order.delivered_time = order.dead_line
        order.save()

def create_today_orders():
    today = timezone.localtime(timezone.now()).date()
    current_local_time = timezone.localtime(timezone.now()).time()

    delivery_schedules = DeliverySchedule.objects.all()
    for ds in delivery_schedules:
        if ds.delivery_schedule.exists():  # используйте `.exists()` для проверки наличия связанных объектов
            for schedule in ds.delivery_schedule.all():
                # если день совпадает с сегодняшним днем
                # и текущее время в промежутке между временем доставки и временем доставки минус 1 час 10 минут
                dt = timezone.localtime(timezone.make_aware(datetime.combine(today, schedule.schedule_time)))
                time_threshold = dt - timedelta(hours=1, minutes=10)
                if str(schedule.day_of_week) == str(today.weekday()) and time_threshold.time() <= current_local_time <= schedule.schedule_time:
                    # создание заказа с учетом временной зоны
                    naive_deadline = datetime.combine(today, schedule.schedule_time)
                    aware_deadline = timezone.make_aware(naive_deadline)
                    order, created = Order.objects.get_or_create(
                        customer=ds.customer,
                        dead_line=aware_deadline
                    )
                    if created:
                        print(f'Создан заказ для {ds.customer.title} на {aware_deadline}')