from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Group, GuestMember

User = get_user_model()

CATEGORY_CHOICES = [
    ('food', 'Nourriture'),
    ('transport', 'Transport'),
    ('accommodation', 'Hébergement'),
    ('entertainment', 'Divertissement'),
    ('shopping', 'Shopping'),
    ('other', 'Autre'),
]


class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_expenses')
    participants = models.ManyToManyField(User, related_name='participated_expenses', blank=True)
    guest_participants = models.ManyToManyField(GuestMember, related_name='participated_expenses', blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.title} — {self.amount}€'
