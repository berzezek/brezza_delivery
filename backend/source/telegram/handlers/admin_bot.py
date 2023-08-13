from aiogram import Router, F
from aiogram.filters import Command, callback_data
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from helpers import (
    get_list_orders, 
    convert_to_hour_minute, 
    get_list_range_possible_orders, 
    adjust_five_hour,
    convert_to_time_string,  
)
from keyboards import buttons
from keyboards.filters import MyCallback

from config import ADMIN_USERS

router = Router()


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    await send_admin_message(message, state)


# Отчет о сегодняшних доставках
@router.callback_query(MyCallback.filter(F.title == "list_today_orders"))
async def list_today_orders(callback: CallbackQuery, state: FSMContext):
    # Получаем список возможных заказов на сегодня
    list_today_orders = await get_list_range_possible_orders('today')

    if not list_today_orders:
        await callback.message.answer("На сегодня заказов нет.")
        return

    # Отправляем сообщение с заказами
    await callback.message.answer("Доставки на сегодня:")
    for entry in list_today_orders:
        customer_name = entry["customer"]
        await callback.message.answer(f"Заказчик {customer_name}:")

        for schedule in entry["delivery_shedule"]:
            schedule_time = schedule["schedule_time"]
            delivered_time = schedule["delivered_time"]
            overdue_time = schedule["overdue_time"]
            # Если нет времени доставки, то ставим значок часов
            status = "\U000023F3"
            if delivered_time:
                status = f"{adjust_five_hour(delivered_time)}"
                if overdue_time:
                    # Если есть время просрочки, то ставим значок восклицательного знака
                    status += f" \U00002757 {convert_to_time_string(overdue_time)} \U00002757"
                else:
                    # Если нет времени просрочки, то ставим значок галочки
                    status += " " + "\U00002705"*3
            await callback.message.answer(f"    {schedule_time[:-3]} - {status}")

@router.callback_query(MyCallback.filter(F.title=="list_month_orders"))
async def list_month_orders(callback: CallbackQuery, state: FSMContext):
    print('list_month_orders')
    await callback.message.answer(text="Список заказов за месяц:")


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