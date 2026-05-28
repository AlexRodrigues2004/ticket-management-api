from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome')
    email = models.EmailField(unique=True, verbose_name='E-mail')
    phone = models.CharField(max_length=20, verbose_name='Telefone')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última atualização')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.email})'