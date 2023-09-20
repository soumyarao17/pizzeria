from background_task import background
from app.models import Order
from django.utils import timezone
from datetime import datetime


@background(schedule=0)
def schedule_order_accepted(order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.status = 'Accepted'
        order.save()
        print(order.id, order.status, datetime.now())
    except Order.DoesNotExist:
        pass

@background(schedule=60)
def schedule_order_preparing(order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.status = 'Preparing'
        order.save()
        print(order.id, order.status, datetime.now())
    except Order.DoesNotExist:
        pass

@background(schedule=180)
def schedule_order_dispatched(order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.status = 'Dispatched'
        order.save()
        print(order.id, order.status, datetime.now())
    except Order.DoesNotExist:
        pass

@background(schedule=300)
def schedule_order_delivered(order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.status = 'Delivered'
        order.save()
        print(order.id, order.status, datetime.now())
    except Order.DoesNotExist:
        pass

def schedule_order_updates(order):
    schedule_order_accepted(order.id)
    schedule_order_preparing(order.id)
    schedule_order_dispatched(order.id)
    schedule_order_delivered(order.id)

def create_order_and_schedule_updates(pizzas):
    try:
        order = Order.objects.create(ordered_at=timezone.now())
        order.pizzas.set(pizzas)
        schedule_order_updates(order)

        return {'success': True, 'order_id': order.id}
    except Exception as e:
        return {'success': False, 'error_message': str(e)}