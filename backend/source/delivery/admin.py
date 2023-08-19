from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from delivery.models import Customer, TgService, Order, Schedule, DeliverySchedule
from django.contrib import admin

admin.site.site_header = "Доставки Brezza laundry"  # измените "Название вашего сайта" на желаемую надпись


admin.site.register(Customer)
# admin.site.register(TgService)
# admin.site.register(Order)
admin.site.register(Schedule)


class ScheduleInline(admin.TabularInline):  # или используйте admin.StackedInline, если вы предпочитаете другой вид
    model = DeliverySchedule.delivery_schedule.through
    extra = 1  # Количество пустых форм, которые будут показаны по умолчанию

@admin.register(DeliverySchedule)
class DeliveryScheduleAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline]
    exclude = ('delivery_schedule',)