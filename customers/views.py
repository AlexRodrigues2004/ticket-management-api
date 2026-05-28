from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Customer
from .serializers import CustomerSerializer
from core.permissions import IsAdminOrAttendant, IsAdminUser


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.action in ('destroy',):
            return [IsAdminUser()]
        if self.action in ('create', 'update', 'partial_update'):
            return [IsAdminOrAttendant()]
        return [IsAuthenticated()]
