import string
import random
from django.db import models
from django.contrib.auth.models import User


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=100)
    image = models.URLField()


    def __str__(self) -> str:
        return self.name
    

class Order(models.Model):
    STATUS = (
        ("Order Recieved", "Order Recieved"),
        ("Baking", "Baking"),
        ("Baked", "Baked"),
        ("Out of delivery", "Out of delivery"),
        ("Order delivered", "Order Delivered")
        )
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    amount = models.FloatField()
    status = models.CharField(max_length=100, choices=STATUS, default="Order Recieved")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.pizza} - Status - {self.status}"

    def generateOrderId(self):
        return ''.join(random.choices(string.ascii_letters, k=7))
    

    def save(self, *args, **kwargs):
        if not self.pk:
            self.order_id = self.generateOrderId()
        super(Order, self).save(*args, **kwargs)

