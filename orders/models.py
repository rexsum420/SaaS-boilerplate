from django.db import models
from django.db.models import F, Sum

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    @property
    def total_sale(self):
        # Aggregate quantity * price directly since 'total' is a property, not a field
        return self.line_items.aggregate(total_sum=Sum(F('quantity') * F('price')))['total_sum'] or 0

    def __str__(self):
        return f"{self.order_id} - {self.status}"


class LineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='line_items')
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"[{self.quantity}] {self.description} x {self.price} = {self.total}"
