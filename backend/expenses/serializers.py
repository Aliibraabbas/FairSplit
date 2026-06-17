from rest_framework import serializers
from django.contrib.auth import get_user_model
from groups.models import GuestMember
from groups.serializers import GuestMemberSerializer
from .models import Expense, CATEGORY_CHOICES

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ExpenseSerializer(serializers.ModelSerializer):
    paid_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    paid_by_detail = UserMinimalSerializer(source='paid_by', read_only=True)
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    participants_detail = UserMinimalSerializer(source='participants', many=True, read_only=True)
    guest_participants = serializers.PrimaryKeyRelatedField(queryset=GuestMember.objects.all(), many=True, required=False)
    guest_participants_detail = GuestMemberSerializer(source='guest_participants', many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Expense
        fields = [
            'id', 'title', 'amount',
            'paid_by', 'paid_by_detail',
            'participants', 'participants_detail',
            'guest_participants', 'guest_participants_detail',
            'group', 'date', 'category', 'category_display',
            'description', 'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['group', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        guest_participants = validated_data.pop('guest_participants', [])
        expense = Expense.objects.create(**validated_data)
        expense.participants.set(participants)
        expense.guest_participants.set(guest_participants)
        return expense

    def update(self, instance, validated_data):
        participants = validated_data.pop('participants', None)
        guest_participants = validated_data.pop('guest_participants', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if participants is not None:
            instance.participants.set(participants)
        if guest_participants is not None:
            instance.guest_participants.set(guest_participants)
        return instance
