from django.shortcuts import render
from .models import Customer, DeliverySchedule, Schedule

def get_customer_schedules():
    data = []

    # Получаем всех заказчиков
    customers = Customer.objects.all()

    for customer in customers:
        customer_data = {}
        customer_data['title'] = customer.title
        customer_data['description'] = customer.description

        # Если у заказчика есть расписание, обработаем его
        try:
            delivery_schedule = DeliverySchedule.objects.get(customer=customer)
            schedules = delivery_schedule.delivery_schedule.all()
            
            # Сначала заполняем все дни недели пустыми строками
            for _, day in Schedule.DAY_OF_WEEK_CHOICE:
                customer_data[day.lower()] = ''
            
            # Теперь заполняем расписанием для каждого дня
            for schedule in schedules:
                day_name = schedule.get_day_of_week_display().lower()
                if customer_data[day_name]:  # Если уже есть запись, добавляем второе время через *
                    customer_data[day_name] += f" • {schedule.convert_to_hour_minute()}"
                else:
                    customer_data[day_name] = schedule.convert_to_hour_minute()

        except DeliverySchedule.DoesNotExist:
            # Если у заказчика нет расписания, пропустим
            pass

        data.append(customer_data)

    return data


def index(request):
    customers = get_customer_schedules()
    return render(request, 'delivery/index.html', {
        'customers': customers
    })