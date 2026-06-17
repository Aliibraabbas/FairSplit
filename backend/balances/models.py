from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Group, GuestMember

User = get_user_model()


class Reimbursement(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='reimbursements')
    from_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='reimbursements_paid')
    from_guest = models.ForeignKey(GuestMember, null=True, blank=True, on_delete=models.CASCADE, related_name='reimbursements_paid')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reimbursements_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
