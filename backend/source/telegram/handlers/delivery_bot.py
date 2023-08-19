from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards.filters import MyCallback
from helpers import (
    get_customers,
    get_customer_by_title,
    set_tg_service,
    get_tg_service_by_tg_id,
    update_tg_service,
    get_today_order_by_customer_title,
    convert_to_hour_minute,
    set_order_delivered_time,
    send_message_to_tg_user
)

from keyboards import (
    buttons
)

router = Router()

# Состояния
class SubscribeFileReceiver(StatesGroup):
    choosing_customer = State() # Выбор заведения
    finished = State() # Завершение

# Обработчики

# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    data = await state.get_data()
    chosen_customer = data.get('chosen_customer')
    chosen_customer_description = data.get('chosen_customer_description')
    if chosen_customer and chosen_customer_description:
        await send_success_subscribe_message(message, state, chosen_customer_description)
    else:
        await send_start_message(message, state)

# Обработчик команды /status
@router.message(Command("status"))
async def cmd_status(message: Message, state: FSMContext):
    data = await state.get_data()
    chosen_customer = data.get('chosen_customer')
    chosen_customer_description = data.get('chosen_customer_description')
    if chosen_customer and chosen_customer_description:
        await send_success_subscribe_message(message, state, chosen_customer_description)
    else:
        await send_start_message(message, state)

# Обработчик состояния выбор заведения
@router.message(SubscribeFileReceiver.choosing_customer)
async def customer_enter(message: Message, state: FSMContext):
    # Получаем список заведений
    customers = await get_customers()
    if not customers:
        await send_subscription_error_message(message, state)
        return

    customers_titles_lower = {customer['title'].lower() for customer in customers}

    # Проверяем введенное заведение
    customer_lower = message.text.lower()
    if customer_lower not in customers_titles_lower:
        await send_no_customer_message(message, state)
        return

    customer = await get_customer_by_title(message.text)
    
    # Назначаем пользователю заведения телеграм сервис
    if not customer:
        await send_no_customer_message(message, state)
        return

    await state.update_data(chosen_customer=customer['title'])
    await state.update_data(chosen_customer_description=customer['description'])
    tg_service = {
        'customer': customer['id'],
        'tg_id': message.chat.id,
        'name': message.from_user.full_name,
        'is_active': True,
    }

    # Проверяем есть ли у пользователя телеграм сервис
    old_tg_service = await get_tg_service_by_tg_id(message.chat.id)
    if old_tg_service:
        # Если есть обновляем
        response = await update_tg_service(tg_service, old_tg_service['id'])
    else:
        # Если нет создаем
        response = await set_tg_service(tg_service)

    if response:
        # Отправляем сообщение о успешной привязке
        await send_success_subscribe_message(message, state, customer['description'])
        await state.set_state(SubscribeFileReceiver.finished)
    else:
        await send_subscription_error_message(message, state)

# TODO Обработчик обрабатывает все заказы за сегодня, нужно исправить
# Callback обработчик кнопки принять заказ
@router.callback_query(MyCallback.filter(F.title=="accept_order"))
async def accept_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    customer = data.get('chosen_customer')
    order = data.get('order')
    if order:
        timenow = datetime.now().strftime("%H:%M")
        await set_order_delivered_time(order['id'])
        await callback.message.answer(
            text=f"Доставка получена в {timenow}"
        )
        # Отправляем сообщение админам
        send_message_to_tg_user(f"Доставка для {customer} обработана в {timenow}")

# Отправляем сообщение о проблеме с привязкой
async def send_subscription_error_message(message: Message, state: FSMContext):
    await message.answer(
        text=f"Привет {message.from_user.full_name}.\n"
            f"есть проблема с привязкой к вашему заведению,\n"
            f"пожалуйста обратитесь в нашу службу поддержки.",
    )
    await state.clear()

# Отправляем сообщение о неправильном заведении
async def send_no_customer_message(message: Message, state: FSMContext):
    await message.answer(
        text=f"Привет {message.from_user.full_name}.\n"
            f"проверьте пожалуйста правильность ввода вашего заведения,\n"
            f"или обратитесь в нашу службу поддержки.",
    )
    await state.clear()

# Отправляем сообщение о начале подписки
async def send_start_message(message: Message, state: FSMContext):
    await message.answer(
        text=f"Привет {message.from_user.full_name}.\n"
            f"Введи пожалуйста свое заведение.\n",
    )
    await state.set_state(SubscribeFileReceiver.choosing_customer)

# Отправляем сообщение о успешной привязке
async def send_success_subscribe_message(message: Message, state: FSMContext, chosen_customer: str):
    await message.answer(
            text=f"Привет {message.from_user.full_name}!\n"
                f"Вы привязаны к заведению {chosen_customer}"
        )
    order = await get_today_order_by_customer_title(chosen_customer)
    if order:
        await state.update_data(order=order)
        await message.answer(
            text=f"Ближайшая доставка в: {convert_to_hour_minute(order['dead_line'])}",
            # accept order button
            reply_markup=buttons.delivery.as_markup()
        )
    else:
        await message.answer(
            text=f"Нет доставки в ближайшее время."
        )