import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app.tasks import schedule_order_accepted, schedule_order_preparing, schedule_order_dispatched, \
    schedule_order_delivered


class OrderStatusTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def mock_create_order(self):
        pizza1 = {'name': 'Pizza 1', 'base': 'thin-crust', 'cheese': 'mozzarella',
                  'toppings': ['pepperoni', 'mushrooms', 'bell-peppers', 'olives', 'onions']}
        pizza2 = {'name': 'Pizza 2', 'base': 'normal', 'cheese': 'cheddar',
                  'toppings': ['pepperoni', 'tomatoes', 'bell-peppers', 'olives', 'sausage']}

        order_data = {
            'pizzas': [pizza1, pizza2],
        }
        response = self.client.post(reverse('app:create-order'), order_data, format='json')
        return response.data.get('order_id')

    def test_order_status_changes(self):
        def get_status_and_assert_order_status_request():
            url = reverse('app:get-order-status', args=[order_id])
            response = self.client.get(url, {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertFalse("error" in response.data)
            self.assertTrue("order_status" in response.data)
            return response.data["order_status"]

        order_id = self.mock_create_order()
        self.assertIsNotNone(order_id)

        schedule_order_accepted.now(order_id)
        self.assertEqual("Accepted", get_status_and_assert_order_status_request())

        schedule_order_preparing.now(order_id)
        self.assertEqual("Preparing", get_status_and_assert_order_status_request())

        schedule_order_dispatched.now(order_id)
        self.assertEqual("Dispatched", get_status_and_assert_order_status_request())

        schedule_order_delivered.now(order_id)
        self.assertEqual("Delivered", get_status_and_assert_order_status_request())


