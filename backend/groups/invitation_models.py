import secrets
from datetime import timedelta
from django.db import models
from django.utils import timezone
from .models import Group


class GroupInvitation(models.Model):
    """Invitation pour rejoindre un groupe via un lien"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='invitations')
    token = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    max_uses = models.IntegerField(default=0)  # 0 = illimité
    uses_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Invitation pour {self.group.name} ({self.token[:8]}...)'

    @classmethod
    def create_invitation(cls, group, days_valid=7, max_uses=0):
        """Crée une nouvelle invitation"""
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(days=days_valid)
        return cls.objects.create(
            group=group,
            token=token,
            expires_at=expires_at,
            max_uses=max_uses
        )

    def is_valid(self):
        """Vérifie si l'invitation est encore valide"""
        if not self.is_active:
            return False
        if timezone.now() > self.expires_at:
            return False
        if self.max_uses > 0 and self.uses_count >= self.max_uses:
            return False
        return True

    def use(self):
        """Incrémente le compteur d'utilisations"""
        self.uses_count += 1
        if self.max_uses > 0 and self.uses_count >= self.max_uses:
            self.is_active = False
        self.save()
