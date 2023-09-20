from rest_framework import serializers
from .models import Pizza, Order
import json

class PizzaSerializer(serializers.ModelSerializer):
    toppings = serializers.SerializerMethodField()

    def get_toppings(self, obj):
        return json.dumps(obj.toppings)

    class Meta:
        model = Pizza
        fields = ['id', 'name', 'base', 'cheese', 'toppings', 'price']

class OrderSerializer(serializers.ModelSerializer):
    pizzas = PizzaSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
