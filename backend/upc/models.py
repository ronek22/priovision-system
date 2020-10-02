from django.db import models
from django.conf import settings


class TypeOfClient(models.TextChoices):
    PRESENT = "OLD", "Present client"
    NEW = "NEW", "New client"

# Create your models here.
class Client(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    number = models.IntegerField(null=False)
    type = models.CharField(max_length=3, choices=TypeOfClient.choices, default=TypeOfClient.NEW)
    core = models.DecimalField(decimal_places=2, max_digits=5)
    premium = models.DecimalField(decimal_places=2, max_digits=5)
    total = models.DecimalField(decimal_places=2, max_digits=5)