from rest_framework import serializers
from .models import Order, LineItem

class LineItemSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = LineItem
        fields = ['id', 'order', 'description', 'quantity', 'price', 'total']

    def get_total(self, obj):
        return obj.total  # Calls the `total` property on LineItem


class OrderSerializer(serializers.ModelSerializer):
    line_items = LineItemSerializer(many=True, read_only=True)
    total_sale = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_id', 'created_at', 'status', 'line_items', 'total_sale']

    def get_total_sale(self, obj):
        return obj.total_sale  # Calls the `total_sale` property on Order
