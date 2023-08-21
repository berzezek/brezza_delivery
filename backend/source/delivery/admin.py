from django.contrib import admin
from delivery.models import Customer, TgService, Order, Schedule, DeliverySchedule
from django.contrib import admin

# измените "Название вашего сайта" на желаемую надпись
admin.site.site_header = "Доставки Brezza laundry"


admin.site.register(Customer)
# admin.site.register(TgService)
admin.site.register(Order)
admin.site.register(Schedule)


# или используйте admin.StackedInline, если вы предпочитаете другой вид
class ScheduleInline(admin.TabularInline):
    model = DeliverySchedule.delivery_schedule.through
    extra = 1  # Количество пустых форм, которые будут показаны по умолчанию


@admin.register(DeliverySchedule)
class DeliveryScheduleAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline]
    exclude = ('delivery_schedule',)
