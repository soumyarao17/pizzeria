from django.utils import timezone
from rest_framework import viewsets
from .models import Pizza, Order
from .serializers import PizzaSerializer, OrderSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.tasks import create_order_and_schedule_updates
import json


class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    @staticmethod
    @api_view(('POST',))
    def create_order_view(request):
        order_data = request.body
        pizzas_data = json.loads(order_data.decode()).get('pizzas', [])
        pizzas = []

        try:
            for pizza_data in pizzas_data:
                pizza = Pizza.objects.create(**pizza_data)
                pizzas.append(pizza)
        except ValueError as e:
            for pizza in pizzas:
                pizza.delete()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        result = create_order_and_schedule_updates(pizzas)
        if result.get('success'):
            return Response({'order_id': result.get('order_id')}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': result.get('error_message')}, status=status.HTTP_400_BAD_REQUEST)


    @staticmethod
    @api_view(('GET',))
    def get_order_status(request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            return Response({'order_id': order_id, 'order_status': order.status}, status=status.HTTP_201_CREATED)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
