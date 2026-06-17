from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Group, CURRENCY_SYMBOLS
from expenses.models import Expense

User = get_user_model()


class CurrencyTestCase(TestCase):
    """Tests pour les devises multiples"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', email='alice@test.com', password='pass123')
        self.user2 = User.objects.create_user(username='bob', email='bob@test.com', password='pass123')
    
    def test_group_default_currency_is_eur(self):
        """Un groupe créé sans devise spécifiée doit avoir EUR par défaut"""
        group = Group.objects.create(
            name='Test Group',
            created_by=self.user1
        )
        self.assertEqual(group.currency, 'EUR')
        self.assertEqual(group.get_currency_symbol(), '€')
    
    def test_group_with_usd_currency(self):
        """Un groupe peut être créé avec la devise USD"""
        group = Group.objects.create(
            name='US Trip',
            currency='USD',
            created_by=self.user1
        )
        self.assertEqual(group.currency, 'USD')
        self.assertEqual(group.get_currency_symbol(), '$')
    
    def test_group_with_gbp_currency(self):
        """Un groupe peut être créé avec la devise GBP"""
        group = Group.objects.create(
            name='London Trip',
            currency='GBP',
            created_by=self.user1
        )
        self.assertEqual(group.currency, 'GBP')
        self.assertEqual(group.get_currency_symbol(), '£')
    
    def test_group_with_lbp_currency(self):
        """Un groupe peut être créé avec la devise LBP"""
        group = Group.objects.create(
            name='Beirut Trip',
            currency='LBP',
            created_by=self.user1
        )
        self.assertEqual(group.currency, 'LBP')
        self.assertEqual(group.get_currency_symbol(), 'ل.ل')
    
    def test_expense_uses_group_currency(self):
        """Une dépense doit utiliser la devise du groupe"""
        group = Group.objects.create(
            name='USD Group',
            currency='USD',
            created_by=self.user1
        )
        group.members.add(self.user1, self.user2)
        
        expense = Expense.objects.create(
            title='Restaurant',
            amount=Decimal('50.00'),
            paid_by=self.user1,
            group=group,
            date='2024-01-15',
            created_by=self.user1
        )
        expense.participants.add(self.user1, self.user2)
        
        # Vérifier que la dépense affiche le bon symbole
        self.assertIn('$', str(expense))
        self.assertEqual(expense.group.currency, 'USD')
    
    def test_all_currency_symbols_defined(self):
        """Tous les symboles de devises doivent être définis"""
        currencies = ['EUR', 'USD', 'GBP', 'LBP']
        for currency in currencies:
            self.assertIn(currency, CURRENCY_SYMBOLS)
            self.assertIsNotNone(CURRENCY_SYMBOLS[currency])
    
    def test_expense_str_with_different_currencies(self):
        """Le __str__ d'une dépense doit afficher la bonne devise"""
        # EUR
        group_eur = Group.objects.create(name='EUR Group', currency='EUR', created_by=self.user1)
        expense_eur = Expense.objects.create(
            title='Café',
            amount=Decimal('5.00'),
            paid_by=self.user1,
            group=group_eur,
            date='2024-01-15',
            created_by=self.user1
        )
        self.assertIn('€', str(expense_eur))
        
        # USD
        group_usd = Group.objects.create(name='USD Group', currency='USD', created_by=self.user1)
        expense_usd = Expense.objects.create(
            title='Coffee',
            amount=Decimal('5.00'),
            paid_by=self.user1,
            group=group_usd,
            date='2024-01-15',
            created_by=self.user1
        )
        self.assertIn('$', str(expense_usd))
