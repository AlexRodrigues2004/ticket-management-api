from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Ticket
from .serializers import TicketSerializer, TicketStatusSerializer
from core.permissions import IsAdminOrAttendant, IsAdminUser


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'category', 'customer']
    search_fields = ['title', 'description']
    ordering_fields = ['opened_at', 'updated_at', 'priority']

    def get_queryset(self):
        user = self.request.user
        if user.role in ('atendente', 'admin'):
            return Ticket.objects.all()
        return Ticket.objects.filter(created_by=user)

    def get_permissions(self):
        if self.action in ('destroy',):
            return [IsAdminUser()]
        if self.action in ('update_status',):
            return [IsAdminOrAttendant()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        ticket = self.get_object()
        serializer = TicketStatusSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
