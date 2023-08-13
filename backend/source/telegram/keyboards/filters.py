from aiogram.filters.callback_data import CallbackData

class MyCallback(CallbackData, prefix='my'):
    title: str

accept_order = MyCallback(title='accept_order')
list_today_orders = MyCallback(title='list_today_orders')
list_month_orders = MyCallback(title='list_month_orders')

# class MyCallback(CallbackData, prefix='my'):
#     foo: str
#     bar: int

# cb1 = MyCallback(foo='demo', bar=42)