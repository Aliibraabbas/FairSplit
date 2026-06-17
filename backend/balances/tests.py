from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from groups.models import Group, GuestMember
from expenses.models import Expense, ExpenseShare
from .services import calculate_balances, calculate_settlements
from datetime import date

User = get_user_model()


class BalanceCalculationTestCase(TestCase):
    """Tests pour le calcul des soldes"""

    def setUp(self):
        # Créer des utilisateurs
        self.alice = User.objects.create_user(username='alice', password='test123')
        self.bob = User.objects.create_user(username='bob', password='test123')
        self.charlie = User.objects.create_user(username='charlie', password='test123')
        
        # Créer un groupe
        self.group = Group.objects.create(
            name='Voyage à Paris',
            created_by=self.alice
        )
        self.group.members.add(self.alice, self.bob, self.charlie)
        
        # Créer un invité
        self.guest = GuestMember.objects.create(group=self.group, name='David')

    def test_equal_split_calculation(self):
        """Test du calcul avec répartition égale"""
        # Alice paie 100€ pour 3 personnes
        expense = Expense.objects.create(
            title='Restaurant',
            amount=Decimal('100.00'),
            paid_by=self.alice,
            group=self.group,
            date=date.today(),
            split_type='equal',
            created_by=self.alice
        )
        expense.participants.add(self.alice, self.bob, self.charlie)
        
        user_balances, guest_balances = calculate_balances(self.group)
        
        # Alice devrait avoir +66.67€ (100 - 33.33)
        alice_balance = next(b for b in user_balances if b['user'].id == self.alice.id)
        self.assertAlmostEqual(float(alice_balance['balance']), 66.67, places=2)
        
        # Bob et Charlie devraient avoir -33.33€ chacun
        bob_balance = next(b for b in user_balances if b['user'].id == self.bob.id)
        charlie_balance = next(b for b in user_balances if b['user'].id == self.charlie.id)
        self.assertAlmostEqual(float(bob_balance['balance']), -33.33, places=2)
        self.assertAlmostEqual(float(charlie_balance['balance']), -33.33, places=2)

    def test_custom_split_calculation(self):
        """Test du calcul avec répartition personnalisée"""
        # Alice paie 100€ mais Bob paie 60€ et Charlie 40€
        expense = Expense.objects.create(
            title='Shopping',
            amount=Decimal('100.00'),
            paid_by=self.alice,
            group=self.group,
            date=date.today(),
            split_type='custom',
            created_by=self.alice
        )
        
        ExpenseShare.objects.create(expense=expense, user=self.bob, amount=Decimal('60.00'))
        ExpenseShare.objects.create(expense=expense, user=self.charlie, amount=Decimal('40.00'))
        
        user_balances, guest_balances = calculate_balances(self.group)
        
        # Alice devrait avoir +100€ (elle a payé mais ne doit rien)
        alice_balance = next(b for b in user_balances if b['user'].id == self.alice.id)
        self.assertEqual(float(alice_balance['balance']), 100.00)
        
        # Bob devrait avoir -60€
        bob_balance = next(b for b in user_balances if b['user'].id == self.bob.id)
        self.assertEqual(float(bob_balance['balance']), -60.00)
        
        # Charlie devrait avoir -40€
        charlie_balance = next(b for b in user_balances if b['user'].id == self.charlie.id)
        self.assertEqual(float(charlie_balance['balance']), -40.00)

    def test_guest_in_equal_split(self):
        """Test avec un invité dans une répartition égale"""
        expense = Expense.objects.create(
            title='Taxi',
            amount=Decimal('40.00'),
            paid_by=self.alice,
            group=self.group,
            date=date.today(),
            split_type='equal',
            created_by=self.alice
        )
        expense.participants.add(self.alice, self.bob)
        expense.guest_participants.add(self.guest)
        
        user_balances, guest_balances = calculate_balances(self.group)
        
        # 40€ / 3 = 13.33€ par personne
        alice_balance = next(b for b in user_balances if b['user'].id == self.alice.id)
        self.assertAlmostEqual(float(alice_balance['balance']), 26.67, places=2)
        
        bob_balance = next(b for b in user_balances if b['user'].id == self.bob.id)
        self.assertAlmostEqual(float(bob_balance['balance']), -13.33, places=2)
        
        # L'invité devrait avoir -13.33€
        self.assertEqual(len(guest_balances), 1)
        self.assertAlmostEqual(float(guest_balances[0]['balance']), -13.33, places=2)


class SettlementCalculationTestCase(TestCase):
    """Tests pour le calcul des remboursements optimisés"""

    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='test123')
        self.bob = User.objects.create_user(username='bob', password='test123')
        self.charlie = User.objects.create_user(username='charlie', password='test123')
        
        self.group = Group.objects.create(
            name='Test Group',
            created_by=self.alice
        )
        self.group.members.add(self.alice, self.bob, self.charlie)

    def test_simple_settlement(self):
        """Test d'un remboursement simple"""
        # Alice paie 90€ pour 3 personnes
        expense = Expense.objects.create(
            title='Dîner',
            amount=Decimal('90.00'),
            paid_by=self.alice,
            group=self.group,
            date=date.today(),
            split_type='equal',
            created_by=self.alice
        )
        expense.participants.add(self.alice, self.bob, self.charlie)
        
        settlements = calculate_settlements(self.group)
        
        # Il devrait y avoir 2 remboursements
        self.assertEqual(len(settlements), 2)
        
        # Bob et Charlie doivent chacun 30€ à Alice
        for settlement in settlements:
            self.assertEqual(settlement['to']['obj'].id, self.alice.id)
            self.assertEqual(float(settlement['amount']), 30.00)

    def test_optimized_settlement(self):
        """Test de l'optimisation des remboursements"""
        # Scénario: Alice paie 100€, Bob paie 50€, tout le monde participe également
        expense1 = Expense.objects.create(
            title='Hôtel',
            amount=Decimal('100.00'),
            paid_by=self.alice,
            group=self.group,
            date=date.today(),
            split_type='equal',
            created_by=self.alice
        )
        expense1.participants.add(self.alice, self.bob, self.charlie)
        
        expense2 = Expense.objects.create(
            title='Essence',
            amount=Decimal('50.00'),
            paid_by=self.bob,
            group=self.group,
            date=date.today(),
            split_type='equal',
            created_by=self.bob
        )
        expense2.participants.add(self.alice, self.bob, self.charlie)
        
        settlements = calculate_settlements(self.group)
        
        # Total: 150€ / 3 = 50€ par personne
        # Alice a payé 100€, doit 50€ → solde +50€
        # Bob a payé 50€, doit 50€ → solde 0€
        # Charlie a payé 0€, doit 50€ → solde -50€
        # Donc Charlie doit 50€ à Alice
        
        self.assertEqual(len(settlements), 1)
        self.assertEqual(settlements[0]['from']['obj'].id, self.charlie.id)
        self.assertEqual(settlements[0]['to']['obj'].id, self.alice.id)
        self.assertEqual(float(settlements[0]['amount']), 50.00)
