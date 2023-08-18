from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from .filters import list_today_orders, list_month_orders, accept_order

delivery = InlineKeyboardBuilder()

delivery.button = InlineKeyboardButton(
    text="Подтвердить получение заказа",
    callback_data=accept_order.pack()
)

delivery.add(delivery.button)

admin = InlineKeyboardBuilder()

admin.button = InlineKeyboardButton(
    text="Отчет сегодня",
    callback_data=list_today_orders.pack()
    )

admin.add(admin.button)

admin.button = InlineKeyboardButton(
    text="Отчет месяц",
    callback_data=list_month_orders.pack()
    )

admin.add(admin.button)




# demo = InlineKeyboardBuilder()
# demo.button = InlineKeyboardButton(
#     text='demo',
#     callback_data=cb1.pack()
# )

# demo.add(demo.button)