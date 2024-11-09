from django.db import models
from orders.models import Order

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)

    def __str_(self):
        return f'Transaction {self.transaction_id} - ${self.amount}'