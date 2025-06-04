from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class AccessRight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=100)
    can_access = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.table_name} - {'OK' if self.can_access else 'No access'}"


class Transaction(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=50)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=30)
    status = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    customer_rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} - {self.amount}€"


class AccessLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(default=now)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    resource = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user} - {self.method} {self.path} at {self.timestamp}"
