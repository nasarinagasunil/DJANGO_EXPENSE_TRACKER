from django.db import models

# Create your models here.

class CurrentBalance(models.Model):
    current_balance = models.FloatField(default=0.0)

class TrackingHistory(models.Model):
    current_balance = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=10, choices=[('DEBIT', 'Debit'), ('CREDIT', 'Credit')])
    amount = models.FloatField()
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)