from delivery.models import Customer, TgService, Order, DeliverySchedule, Schedule
from rest_framework import serializers
from django.utils import timezone


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class TgServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgService
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderGetSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.title')
    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'dead_line',
            'delivered_time',
            'overdue_time',
        )

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class ScheduleWithOrderInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = '__all__'


class DeliveryScheduleSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.title')
    delivery_schedule = serializers.SerializerMethodField()
    
    class Meta:
        model = DeliverySchedule
        fields = (
            'id',
            'customer',
            'delivery_schedule',
        )

    def get_delivery_schedule(self, obj):
        # Если в контексте сериализатора передан параметр range со значением 'today'
        if self.context.get('request') and self.context['request'].GET.get('range') == 'today':
            current_weekday = str(timezone.localtime(timezone.now()).weekday())
            schedules_for_today = obj.delivery_schedule.filter(day_of_week=current_weekday)
        else:
            schedules_for_today = obj.delivery_schedule.all()

        return ScheduleWithOrderInfoSerializer(schedules_for_today, many=True).data
