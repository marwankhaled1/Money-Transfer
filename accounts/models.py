from django.db import models

class Account(models.Model):
    Account_ID = models.CharField(max_length=100, unique=True,primary_key=True)
    Name = models.CharField(max_length=255)
    Balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.Name} ({self.Account_ID})"