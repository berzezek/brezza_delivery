from datetime import datetime, timedelta, timezone
import aiohttp
from functools import wraps
import requests
from config import TELEGRAM_BOT_TOKEN, ADMIN_USERS, HOST_URL


# Отправка сообщения в телеграм администраторам
def send_message_to_tg_user(text):
    for admin in ADMIN_USERS:
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        data = {
            'chat_id': admin,
            'text': text,
        }
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return True
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")


def aiohttp_session(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await func(session, *args, **kwargs)
    return wrapped


# helpers for delivery_bot

# Получение списка заказчиков
@aiohttp_session
async def get_customers(session):
    try:
        async with session.get(f'{HOST_URL}/api/v1/customers/') as response:
            if response.status == 200:
                customers = await response.json()
                return customers
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
    return None

# Получение заказчика по названию


@aiohttp_session
async def get_customer_by_title(session, title: str):
    try:
        async with session.get(f'{HOST_URL}/api/v1/customers?title={title}') as response:
            if response.status == 200:
                customer = await response.json()
                if len(customer) > 0:
                    return customer[0]
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
    return None

# Установка сервиса телеграм


@aiohttp_session
async def set_tg_service(session, tg_service: dict):
    try:
        async with session.post(f'{HOST_URL}/api/v1/tgservices/', json=tg_service) as response:
            if response.status == 201:
                tg_service = await response.json()
                return tg_service
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
    return None

# Получение сервиса телеграм по id


@aiohttp_session
async def get_tg_service_by_tg_id(session, tg_id: str or int):
    try:
        async with session.get(f'{HOST_URL}/api/v1/tgservices?tg_id={tg_id}') as response:
            if response.status == 200:
                tg_service = await response.json()
                if len(tg_service) > 0:
                    return tg_service[0]
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
    return None

# Удаление сервиса телеграм по id


@aiohttp_session
async def remove_tg_service_by_tg_id(session, tg_id):
    try:
        async with session.delete(f'{HOST_URL}/api/v1/tgservices?tg_id={tg_id}') as response:
            if response.status == 204:
                return True
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
    return None

# Обновление сервиса телеграм по id


@aiohttp_session
async def update_tg_service(session, tg_service: dict, tg_service_id: int):
    try:
        async with session.patch(f'{HOST_URL}/api/v1/tgservices/{tg_service_id}/', json=tg_service) as response:
            if response.status == 200:
                tg_service = await response.json()
                return tg_service
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
    return None

# Получение деталей заказчика по id


@aiohttp_session
async def get_customer_by_id(session, customer_id: int):
    try:
        async with session.get(f'{HOST_URL}/api/v1/customers/{customer_id}/') as response:
            if response.status == 200:
                customer = await response.json()
                return customer
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
    return None


# helpers for admin

# Получение списка заказов за период (today)
@aiohttp_session
async def get_list_orders(session, range: str):
    try:
        async with session.get(f'{HOST_URL}/api/v1/orders?range={range}') as response:
            if response.status == 200:
                shipments = await response.json()
                return shipments
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
    return None

# Получение сегодняшнего заказа по названию заказчика


@aiohttp_session
async def get_today_order_by_customer_title(session, customer_title: int):
    try:
        async with session.get(f'{HOST_URL}/api/v1/orders?customer={customer_title}&list=today') as response:
            if response.status == 200:
                orders = await response.json()
                if len(orders) > 0:
                    order = orders[0]
                    if order.get('delivered_time') is None:
                        return order
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
    return None


def convert_to_hour_minute(datetime_str: str) -> str:
    # '2023-08-13T07:00:00+05:00' -> '07:00'
    try:
        time_hour_minute = datetime.strptime(
            datetime_str, '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')
        return time_hour_minute
    except:
        return None

# Установка веремени получения заказа


@aiohttp_session
async def set_order_delivered_time(session, order_id: int, receiver_name: str):
    try:
        delivered_time_str = datetime.now(timezone.utc).isoformat()
        async with session.patch(f'{HOST_URL}/api/v1/orders/{order_id}/', json={
            'delivered_time': delivered_time_str,
            'receiver_name': receiver_name,
        }) as response:

            if response.status == 200:
                order = await response.json()
                return order
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
    return None

# Список возможных заказов на сегодня


@aiohttp_session
async def get_list_range_possible_orders(session, range: str):
    try:
        async with session.get(f'{HOST_URL}/api/v1/deliveryschedules/?range={range}') as response:
            if response.status == 200:
                possible_orders = await response.json()
                return possible_orders
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
    return None

# Прибавляем к вренмени 5 часов и преобразуем в час:мин


def adjust_five_hour(date_str: str) -> str:
    try:
        if date_str.endswith("Z"):
            date_str = date_str[:-1]

        dt = datetime.fromisoformat(date_str) + timedelta(hours=5)
        formatted_time = dt.strftime('%H:%M')
        return formatted_time
    except Exception as e:
        print(f"Error: {e}")
        return None

# Вместо timedelta возвращаем строку вида 00:00


def convert_to_time_string(value: str):
    try:
        # Преобразование строки в объект timedelta
        hours, minutes, seconds = map(float, value.split(':'))
        total_seconds = int(hours * 3600 + minutes * 60 + seconds)

        # Получение часов и минут из общего количества секунд
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02}:{minutes:02}"
    except:
        return None


def convert_second_to_hour_minute(value: int):
    try:
        # Получение часов и минут из общего количества секунд
        hours = value // 3600
        minutes = (value % 3600) // 60
        return f"{hours:02}:{minutes:02}"
    except:
        return None

# Получение сегодняшнего заказа по названию заказчика и времени доставки


@aiohttp_session
async def get_today_order_by_customer_title_and_schedule_time(session, customer_title: str, schedule_time: str):
    try:
        async with session.get(f'{HOST_URL}/api/v1/orders?customer={customer_title}&list=today&schedule_time={schedule_time}') as response:
            if response.status == 200:
                possible_orders = await response.json()
                if len(possible_orders) > 0:
                    return possible_orders[0]
            else:
                print(f"Error: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
    return None

# Преобразование строки в секунды


def time_to_seconds(timestr: str) -> int:
    hours, minutes, seconds = timestr.split(':')
    return int(hours) * 3600 + int(minutes) * 60 + int(float(seconds))
