from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .serializers import CategorySerializer
from core.permissions import IsAdminOrAttendant, IsAdminUser


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ('destroy',):
            return [IsAdminUser()]
        if self.action in ('create', 'update', 'partial_update'):
            return [IsAdminOrAttendant()]
        return [IsAuthenticated()]
