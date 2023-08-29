from delivery.models import Customer, TgService, Order, DeliverySchedule, Schedule
from delivery.api.serializers import (
    CustomerSerializer, 
    TgServiceSerializer, 
    OrderSerializer, 
    OrderGetSerializer,
    DeliveryScheduleSerializer
)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone
from django.db.models.functions import ExtractWeekDay
import pytz
from django.db.models import IntegerField




class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        customer_title = request.GET.get('title')
        if customer_title:
            # Искать по title без учета регистра
            queryset = Customer.objects.filter(title__iexact=customer_title)
        else:
            queryset = Customer.objects.all()
        serializer = self.get_serializer(queryset, many=True)  # Добавление many=True
        return Response(serializer.data)



class TgServiceViewSet(viewsets.ModelViewSet):
    queryset = TgService.objects.all()
    serializer_class = TgServiceSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        tg_id = request.GET.get('tg_id')
        if tg_id:
            queryset = TgService.objects.filter(tg_id=tg_id)
        else:
            queryset = TgService.objects.all()
        serializer = self.get_serializer(queryset, many=True)  # Добавление many=True
        return Response(serializer.data)
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super(OrderViewSet, self).get_queryset()
        return queryset.select_related('customer')

    def list(self, request):
        list_range = request.GET.get('list')  # Используйте 'list' вместо 'range'
        customer = request.GET.get('customer')
        delivered = request.GET.get('delivered')
        schedule_time = request.GET.get('schedule_time')
        queryset = self.get_queryset()
        if customer:
            queryset = queryset.filter(customer__title__iexact=customer)
        if list_range == 'today':
            today_weekday = datetime.now(pytz.timezone('Asia/Tashkent')).isoweekday() % 7 + 1  # Convert to Django's week day numbering
            # filter queryset must be gte today
            queryset = queryset.filter(dead_line__gte=datetime.now(pytz.timezone('Asia/Tashkent')))
            queryset = queryset.annotate(weekday=ExtractWeekDay('dead_line', output_field=IntegerField())).filter(weekday=today_weekday)
        elif list_range == 'yesterday':
            today_weekday = datetime.now(pytz.timezone('Asia/Tashkent')).isoweekday() % 7 + 1  # Convert to Django's week day numbering
            yesterday_weekday = today_weekday - 1
            queryset = queryset.annotate(weekday=ExtractWeekDay('dead_line', output_field=IntegerField())).filter(weekday=yesterday_weekday)
        if delivered == 'false':
            queryset = queryset.filter(delivered_time__isnull=True)
        if schedule_time:
            hour, minute = map(int, schedule_time.split(":"))
            queryset = queryset.filter(dead_line__hour=hour, dead_line__minute=minute)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class DeliveryScheduleViewSet(viewsets.ModelViewSet):
    queryset = DeliverySchedule.objects.all()
    serializer_class = DeliveryScheduleSerializer

    def get_queryset(self):
        queryset = super(DeliveryScheduleViewSet, self).get_queryset()
        return queryset.select_related('customer').prefetch_related('delivery_schedule')

    def list(self, request):
        queryset = self.get_queryset()
        list_range = request.GET.get('range')
        if list_range == 'today':
            current_weekday = str(timezone.localtime(timezone.now()).weekday())
            schedules_for_today = Schedule.objects.filter(day_of_week=current_weekday)
            queryset = queryset.filter(delivery_schedule__in=schedules_for_today).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
