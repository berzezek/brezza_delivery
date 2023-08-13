from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.utils.formatting import Text
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


class SubscribeFileReceiver(StatesGroup):
    choosing_customer = State()
    finished = State()

async def send_subscription_error_message(message: Message, state: FSMContext):
    await message.answer(
        text=f"Привет {message.from_user.full_name}.\n"
            f"есть проблема с привязкой к вашему заведению,\n"
            f"пожалуйста обратитесь в нашу службу поддержки.",
    )
    await state.clear()

async def send_no_customer_message(message: Message, state: FSMContext):
    await message.answer(
        text=f"Привет {message.from_user.full_name}.\n"
            f"проверьте пожалуйста правильность ввода вашего заведения,\n"
            f"или обратитесь в нашу службу поддержки.",
    )
    await state.clear()

async def send_start_message(message: Message, state: FSMContext):
    await message.answer(
        text=f"Привет {message.from_user.full_name}.\n"
            f"Введи пожалуйста свое заведение.\n",
    )
    await state.set_state(SubscribeFileReceiver.choosing_customer)

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


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    data = await state.get_data()
    chosen_customer = data.get('chosen_customer')
    if chosen_customer:
        await send_success_subscribe_message(message, state, chosen_customer)
    else:
        await send_start_message(message, state)


@router.message(Command("status"))
async def cmd_status(message: Message, state: FSMContext):
    data = await state.get_data()
    chosen_customer = data.get('chosen_customer')
    if chosen_customer:
        await send_success_subscribe_message(message, state, chosen_customer)
    else:
        await send_start_message(message, state)


@router.message(SubscribeFileReceiver.choosing_customer)
async def customer_enter(message: Message, state: FSMContext):
    # get all customers
    customers = await get_customers()
    if customers:
        customers_titles = [customer['title'] for customer in customers]
        # check if message.text in customers_titles
        if message.text in customers_titles:
            await state.update_data(chosen_customer=message.text)
            customer = await get_customer_by_title(message.text)
            # set new tg_service
            tg_service = {
                'customer': customer['id'],
                'tg_id': message.chat.id,
                'name': message.from_user.full_name,
                'is_active': True,
            }
            # update old tg_service
            old_tg_service = await get_tg_service_by_tg_id(message.chat.id)
            if old_tg_service:
                response = await update_tg_service(tg_service, old_tg_service['id'])
            else:
                response = await set_tg_service(tg_service)
            if response:
                await send_success_subscribe_message(message, state, message.text)
                await state.set_state(SubscribeFileReceiver.finished)
            else:
                await send_subscription_error_message(message, state)
        else:
            await send_no_customer_message(message, state)
    else:
        await send_subscription_error_message(message, state)


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
        # send message to admins
        send_message_to_tg_user(f"Доставка для {customer} обработана в {timenow}")

