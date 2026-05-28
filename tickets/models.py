from django.db import models
from django.conf import settings
from customers.models import Customer
from categories.models import Category


class Ticket(models.Model):

    class Status(models.TextChoices):
        ABERTO = 'aberto', 'Aberto'
        EM_ATENDIMENTO = 'em_atendimento', 'Em Atendimento'
        AGUARDANDO_CLIENTE = 'aguardando_cliente', 'Aguardando Cliente'
        RESOLVIDO = 'resolvido', 'Resolvido'
        CANCELADO = 'cancelado', 'Cancelado'

    class Priority(models.TextChoices):
        BAIXA = 'baixa', 'Baixa'
        MEDIA = 'media', 'Média'
        ALTA = 'alta', 'Alta'
        CRITICA = 'critica', 'Crítica'

    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name='Cliente'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tickets',
        verbose_name='Categoria'
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.ABERTO,
        verbose_name='Status'
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIA,
        verbose_name='Prioridade'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets',
        verbose_name='Responsável'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tickets',
        verbose_name='Criado por'
    )
    opened_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de abertura')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última atualização')

    class Meta:
        verbose_name = 'Chamado'
        verbose_name_plural = 'Chamados'
        ordering = ['-opened_at']

    def __str__(self):
        return f'#{self.pk} - {self.title} [{self.get_status_display()}]'