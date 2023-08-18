from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from datetime import datetime


from helpers import (
    get_list_range_possible_orders,
    convert_to_time_string,
    get_today_order_by_customer_title_and_schedule_time,
    time_to_seconds,
    convert_second_to_hour_minute,
)
from keyboards import buttons
from keyboards.filters import MyCallback

from config import ADMIN_USERS

router = Router()

# Вход в админ панель
@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    await send_admin_message(message, state)

# Обработчики

# TODO исправить delivered_time
# Отчет о сегодняшних доставках
@router.callback_query(MyCallback.filter(F.title == "list_today_orders"))
async def list_today_orders(callback: CallbackQuery, state: FSMContext):
    # Получаем список возможных заказов на сегодня
    list_today_possible_orders = await get_list_range_possible_orders('today')

    if not list_today_possible_orders:
        await callback.message.answer("На сегодня заказов нет.")
        return

    # Формирование сообщения с заказами
    message_text = "Доставки на сегодня:\n\n"
    for possible_order in list_today_possible_orders:
        customer_name = possible_order.get("customer")
        schedules_text = f"Заказчик {customer_name}:\n"
        for schedule in possible_order.get("delivery_schedule"):
            schedule_time = schedule.get("schedule_time")
            # Найти сегодняшний заказ с таким же временем
            today_order = await get_today_order_by_customer_title_and_schedule_time(customer_name, schedule_time[0:-3])
            if today_order:
                delivered_time = today_order.get("delivered_time")
                overdue_time = today_order.get("overdue_time")
            else:
                delivered_time = None
                overdue_time = None

            if not delivered_time:
                status = "\U000023F3"  # Значок часов, если нет времени доставки
            else:
                status = f"{datetime.fromisoformat(delivered_time).strftime('%H:%M')}"
                if overdue_time:
                    # Если есть время просрочки, добавляем значок восклицательного знака
                    status += f" \U00002757 {convert_to_time_string(overdue_time)} \U00002757"
                    # '00:49:10.420511' to seconds 
                    
                else:
                    # Если нет времени просрочки, добавляем значок галочки
                    status += " " + "\U00002705  " * 3
            schedules_text += f"• {schedule_time[:-3]} - {status}\n"

        message_text += schedules_text + "\n"
    

    await callback.message.answer(message_text)


# Отчет о доставках за месяц
@router.callback_query(MyCallback.filter(F.title == "list_month_orders"))
async def list_month_orders(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Список заказов за месяц: (в разработке)")


# Сообщения при входе через /admin
async def send_admin_message(message: Message, _state: FSMContext):
    # Проверка на админа
    if str(message.chat.id) in ADMIN_USERS:
        await message.answer(
            text=f"Привет {message.from_user.full_name}.\nВы зашли в админ панель.\n",
            reply_markup=buttons.admin.as_markup(),
        )
    else:
        await message.answer(
            text=f"Привет {message.from_user.full_name}.\n"
            f"Вы не имеете доступа к админ панели.\n"
            f"Обратитесь к нашей службе поддрежки.",
            reply_markup=ReplyKeyboardRemove()
        )
