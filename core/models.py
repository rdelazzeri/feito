from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        'criado em',
        blank=True, null=True,
        auto_now_add=True,
        auto_now=False
    )
    modified = models.DateTimeField(
        'modificado em',
        blank=True, null=True,
        auto_now_add=False,
        auto_now=True
    )

    class Meta:
        abstract = True


class LogModel(models.Model):
    criado = models.DateTimeField(auto_now_add=True)
    criadoPor = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    modificado = models.DateTimeField(auto_now=True)
    modificadoPor = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)

    class Meta:
        abstract = True