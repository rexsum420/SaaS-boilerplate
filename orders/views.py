from rest_framework import viewsets
from .models import Order, LineItem
from .serializers import OrderSerializer, LineItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from saas.context_processor import get_role

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if get_role(self.request.user) in ['Admin', 'Owner', 'Manager', 'Employee']:
            return super().perform_create(serializer)
        raise PermissionDenied('Must be on staff to create an order')
    
    def perform_update(self, serializer):
        if get_role(self.request.user) in ['Admin', 'Owner', 'Manager']:
            return super().perform_update(serializer)
        raise PermissionDenied('Must be part of management in order to change order details')
    
    def perform_destroy(self, instance):
        if get_role(self.request.user) in ['Admin', 'Owner']:
            return super().perform_destroy(instance)
        raise PermissionDenied('Must be part of admin/owner in order to delete order details')

class LineItemViewSet(viewsets.ModelViewSet):
    queryset = LineItem.objects.all()
    serializer_class = LineItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
