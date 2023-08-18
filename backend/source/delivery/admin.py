from django.contrib import admin
from delivery.models import Customer, TgService, Order, Schedule, DeliverySchedule

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