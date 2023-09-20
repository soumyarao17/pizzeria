import django
from django.db import models
from django.utils import timezone

from app.constants import BASE_CHOICES, CHEESE_CHOICES, TOPPING_CHOICES, STATUS_CHOICES


class Pizza(models.Model):
    name = models.CharField(default="Pizzeria", max_length=255)
    base = models.CharField(null=False, max_length=15, choices=BASE_CHOICES)
    cheese = models.CharField(null=False, max_length=15, choices=CHEESE_CHOICES)
    toppings = models.JSONField(default=list, choices=TOPPING_CHOICES)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=100.0)

    def save(self, *args, **kwargs):
        if not isinstance(self.toppings, list) or len(set(self.toppings)) != 5:
            raise ValueError("You must select 5 toppings.")

        topping_choices = [topping[0] for topping in TOPPING_CHOICES]
        for topping_choice in self.toppings:
            if topping_choice not in topping_choices:
                raise ValueError(f"You must select 5 toppings amongst {topping_choices}.")

        cheese_choices = [cheese[0] for cheese in CHEESE_CHOICES]
        if self.cheese not in cheese_choices:
            raise ValueError(f"You must select 1 cheese amongst {cheese_choices}.")

        base_choices = [base[0] for base in BASE_CHOICES]
        if self.base not in base_choices:
            raise ValueError(f"You must select 1 base amongst {base_choices}.")
        super().save(*args, **kwargs)

class Order(models.Model):
    pizzas = models.ManyToManyField(Pizza, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Placed')
    ordered_at = models.DateTimeField(default=django.utils.timezone.now)

