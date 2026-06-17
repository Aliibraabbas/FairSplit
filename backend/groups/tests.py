from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Group, GroupInvitation

User = get_user_model()


class GroupInvitationTestCase(TestCase):
    """Tests pour les invitations de groupe"""

    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='test123')
        self.bob = User.objects.create_user(username='bob', password='test123')
        
        self.group = Group.objects.create(
            name='Test Group',
            created_by=self.alice
        )
        self.group.members.add(self.alice)

    def test_create_invitation(self):
        """Test de création d'une invitation"""
        invitation = GroupInvitation.create_invitation(self.group, days_valid=7)
        
        self.assertIsNotNone(invitation.token)
        self.assertEqual(len(invitation.token), 43)  # token_urlsafe(32) génère 43 caractères
        self.assertEqual(invitation.group, self.group)
        self.assertTrue(invitation.is_active)
        self.assertEqual(invitation.uses_count, 0)
        self.assertTrue(invitation.is_valid())

    def test_invitation_expiration(self):
        """Test de l'expiration d'une invitation"""
        # Créer une invitation qui expire dans le passé
        invitation = GroupInvitation.objects.create(
            group=self.group,
            token='test-token-expired',
            expires_at=timezone.now() - timedelta(days=1),
            is_active=True
        )
        
        self.assertFalse(invitation.is_valid())

    def test_invitation_max_uses(self):
        """Test de la limite d'utilisations"""
        invitation = GroupInvitation.create_invitation(self.group, max_uses=2)
        
        # Première utilisation
        invitation.use()
        self.assertEqual(invitation.uses_count, 1)
        self.assertTrue(invitation.is_valid())
        self.assertTrue(invitation.is_active)
        
        # Deuxième utilisation
        invitation.use()
        self.assertEqual(invitation.uses_count, 2)
        self.assertFalse(invitation.is_active)
        self.assertFalse(invitation.is_valid())

    def test_invitation_unlimited_uses(self):
        """Test d'une invitation sans limite d'utilisations"""
        invitation = GroupInvitation.create_invitation(self.group, max_uses=0)
        
        # Utiliser plusieurs fois
        for i in range(10):
            invitation.use()
        
        self.assertEqual(invitation.uses_count, 10)
        self.assertTrue(invitation.is_active)
        self.assertTrue(invitation.is_valid())

    def test_deactivated_invitation(self):
        """Test d'une invitation désactivée"""
        invitation = GroupInvitation.create_invitation(self.group)
        invitation.is_active = False
        invitation.save()
        
        self.assertFalse(invitation.is_valid())
