from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        ATENDENTE = 'atendente', 'Atendente'
        ADMIN = 'admin', 'Administrador'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENTE,
    )

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
