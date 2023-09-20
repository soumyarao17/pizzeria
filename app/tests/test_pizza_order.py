from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app.models import Pizza, Order


class OrderCreationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_pizza_order(self):
        pizza1 = {'name': 'Pizza 1', 'base': 'thin-crust', 'cheese': 'mozzarella',
                  'toppings': ['pepperoni', 'mushrooms', 'bell-peppers', 'olives', 'onions'],
                  'price': 70}
        pizza2 = {'name': 'Pizza 2', 'base': 'normal', 'cheese': 'cheddar',
                  'toppings': ['pepperoni', 'tomatoes', 'bell-peppers', 'olives', 'sausage'],
                  'price': 90}

        order_data = {
            'pizzas': [pizza1, pizza2],
        }
        response = self.client.post(reverse('app:create-order'), order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().pizzas.count(), 2)

    def test_invalid_toppings_save(self):
        # Create a pizza with less than 5 toppings
        pizza_data_1 = {'name': 'Pizza 2', 'base': 'normal', 'cheese': 'cheddar',
                        'toppings': ['pepperoni', 'tomatoes', 'bell-peppers', 'olives', 'sausage'],
                        'price': 90}
        pizza_data_2 = {
            'name': 'Test Pizza',
            'base': 'thin-crust',
            'cheese': 'mozzarella',
            'toppings': ['pepperoni', 'mushrooms']  # Less than 5 toppings
        }

        order_data = {
            'pizzas': [pizza_data_1, pizza_data_2],
        }

        response = self.client.post(reverse('app:create-order'), order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You must select 5 toppings.")
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(Pizza.objects.count(), 0)

