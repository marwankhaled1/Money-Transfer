from django.db import models
from accounts.models import Account

class Transfer(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transfers')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_transfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)