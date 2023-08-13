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
import datetime
from django.utils import timezone


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        customer_title = request.GET.get('title')
        if customer_title:
            queryset = Customer.objects.filter(title=customer_title)
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
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderGetSerializer
        return super().get_serializer_class()

    def list(self, request):
        # get today orders
        list_range = request.GET.get('range')
        customer = request.GET.get('customer')
        delivered = request.GET.get('delivered')
        queryset = Order.objects.all()
        if customer:
            queryset = queryset.filter(customer__title=customer)
        if list_range == 'today':
            today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = queryset.filter(dead_line__gte=today)
        if delivered == 'false':
            queryset = queryset.filter(delivered_time__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DeliveryScheduleViewSet(viewsets.ModelViewSet):
    queryset = DeliverySchedule.objects.all()
    serializer_class = DeliveryScheduleSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        queryset = DeliverySchedule.objects.all()
        list_range = request.GET.get('range')
        if list_range == 'today':
            # Получить текущий день недели
            current_weekday = str(timezone.localtime(timezone.now()).weekday())
            # Найти все записи `Schedule` для этого дня недели
            schedules_for_today = Schedule.objects.filter(day_of_week=current_weekday)
            # Найти все записи `DeliverySchedule`, которые содержат найденные записи `Schedule`
            queryset = DeliverySchedule.objects.filter(delivery_shedule__in=schedules_for_today).distinct()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)