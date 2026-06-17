from rest_framework import serializers
from .models import Reimbursement


class ReimbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reimbursement
        fields = ['id', 'from_user', 'from_guest', 'to_user', 'amount', 'created_at']
