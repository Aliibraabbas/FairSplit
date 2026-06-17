from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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

SPLIT_TYPE_CHOICES = [
    ('equal', 'Répartition égale'),
    ('custom', 'Répartition personnalisée'),
]


class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_expenses')
    participants = models.ManyToManyField(User, related_name='participated_expenses', blank=True)
    guest_participants = models.ManyToManyField(GuestMember, related_name='guest_participated_expenses', blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True)
    split_type = models.CharField(max_length=20, choices=SPLIT_TYPE_CHOICES, default='equal')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        currency_symbol = self.group.get_currency_symbol()
        return f'{self.title} — {self.amount}{currency_symbol}'


class ExpenseShare(models.Model):
    """Représente la part personnalisée d'un participant dans une dépense"""
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='custom_shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest = models.ForeignKey(GuestMember, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = [['expense', 'user'], ['expense', 'guest']]

    def clean(self):
        if self.user and self.guest:
            raise ValidationError("Une part ne peut pas avoir à la fois un user et un guest")
        if not self.user and not self.guest:
            raise ValidationError("Une part doit avoir soit un user soit un guest")
        if self.amount < 0:
            raise ValidationError("Le montant ne peut pas être négatif")

    def __str__(self):
        participant = self.user.username if self.user else self.guest.name
        currency_symbol = self.expense.group.get_currency_symbol()
        return f'{participant} — {self.amount}{currency_symbol}'
