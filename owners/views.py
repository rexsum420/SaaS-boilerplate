from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from saas.context_processor import get_role
from owners.models import Owner
from owners.serializers import OwnerSerializer

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            role = get_role(self.request.user)
            if role in ['Owner', 'Admin']:            
                owners = Owner.objects.all()
                qs = owners
                return qs
        return None
    
    def perform_create(self, serializer):
        if self.request.user.role in ['Owner', 'Admin']:
            raise PermissionDenied("Only owners and admins can create owner accounts.")