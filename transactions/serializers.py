from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'created_at', 'order', 'amount', 'status', 'payment_method']
        read_only_fields = ['transaction_id', 'created_at', 'order', 'amount', 'status', 'payment_method']

    def validate(self, attrs):
        # Check if the instance exists and its status is 'complete'
        if self.instance and self.instance.status == 'complete':
            # Make all fields read-only if status is complete
            raise serializers.ValidationError("This transaction is complete and cannot be modified.")
        return attrs
