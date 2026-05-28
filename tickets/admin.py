from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'customer', 'category', 'status', 'priority', 'assigned_to', 'opened_at')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('title', 'description')
