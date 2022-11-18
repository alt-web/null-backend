from django.db import models

# Create your models here.
class Board(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=256)

    def __str__(self):
        return f'/{self.code}/ - {self.name}'
