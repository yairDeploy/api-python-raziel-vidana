from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    edad = models.IntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    # El resto de campos (nombre, apellido, email, etc.) ya los incluye AbstractUser
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username