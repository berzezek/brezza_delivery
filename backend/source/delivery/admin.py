from django.contrib import admin
from delivery.models import Customer, TgService, Order, Schedule, DeliverySchedule

admin.site.register(Customer)
admin.site.register(TgService)
admin.site.register(Order)
admin.site.register(Schedule)
admin.site.register(DeliverySchedule)