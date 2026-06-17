from rest_framework import serializers
from django.contrib.auth import get_user_model
from decimal import Decimal
from groups.models import GuestMember
from groups.serializers import GuestMemberSerializer
from .models import Expense, ExpenseShare, CATEGORY_CHOICES

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ExpenseShareSerializer(serializers.Serializer):
    """Serializer pour les parts personnalisées"""
    user_id = serializers.IntegerField(required=False, allow_null=True)
    guest_id = serializers.IntegerField(required=False, allow_null=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        if not data.get('user_id') and not data.get('guest_id'):
            raise serializers.ValidationError("Une part doit avoir soit un user_id soit un guest_id")
        if data.get('user_id') and data.get('guest_id'):
            raise serializers.ValidationError("Une part ne peut pas avoir à la fois un user_id et un guest_id")
        if data['amount'] < 0:
            raise serializers.ValidationError("Le montant ne peut pas être négatif")
        return data


class ExpenseSerializer(serializers.ModelSerializer):
    paid_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    paid_by_detail = UserMinimalSerializer(source='paid_by', read_only=True)
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
    participants_detail = UserMinimalSerializer(source='participants', many=True, read_only=True)
    guest_participants = serializers.PrimaryKeyRelatedField(queryset=GuestMember.objects.all(), many=True, required=False)
    guest_participants_detail = GuestMemberSerializer(source='guest_participants', many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    split_type_display = serializers.CharField(source='get_split_type_display', read_only=True)
    custom_shares = ExpenseShareSerializer(many=True, required=False, write_only=True)
    custom_shares_detail = serializers.SerializerMethodField(read_only=True)
    currency = serializers.CharField(source='group.currency', read_only=True)
    currency_symbol = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Expense
        fields = [
            'id', 'title', 'amount', 'currency', 'currency_symbol',
            'paid_by', 'paid_by_detail',
            'participants', 'participants_detail',
            'guest_participants', 'guest_participants_detail',
            'group', 'date', 'category', 'category_display',
            'description', 'split_type', 'split_type_display',
            'custom_shares', 'custom_shares_detail',
            'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['group', 'created_by', 'created_at', 'updated_at']
    
    def get_currency_symbol(self, obj):
        return obj.group.get_currency_symbol()

    def get_custom_shares_detail(self, obj):
        if obj.split_type != 'custom':
            return []
        shares = obj.custom_shares.select_related('user', 'guest').all()
        return [
            {
                'user_id': share.user.id if share.user else None,
                'guest_id': share.guest.id if share.guest else None,
                'username': share.user.username if share.user else share.guest.name,
                'amount': str(share.amount),
            }
            for share in shares
        ]

    def validate(self, data):
        split_type = data.get('split_type', 'equal')
        custom_shares = data.get('custom_shares', [])

        if split_type == 'custom':
            if not custom_shares:
                raise serializers.ValidationError("Les parts personnalisées sont requises pour une répartition personnalisée")
            
            total_shares = sum(Decimal(str(share['amount'])) for share in custom_shares)
            expense_amount = data.get('amount', self.instance.amount if self.instance else 0)
            
            if abs(total_shares - expense_amount) > Decimal('0.01'):
                raise serializers.ValidationError(
                    f"Le total des parts ({total_shares}€) doit être égal au montant de la dépense ({expense_amount}€)"
                )
        
        return data

    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        guest_participants = validated_data.pop('guest_participants', [])
        custom_shares = validated_data.pop('custom_shares', [])
        
        expense = Expense.objects.create(**validated_data)
        
        if expense.split_type == 'equal':
            expense.participants.set(participants)
            expense.guest_participants.set(guest_participants)
        else:
            # Pour custom, on crée les ExpenseShare
            for share_data in custom_shares:
                ExpenseShare.objects.create(
                    expense=expense,
                    user_id=share_data.get('user_id'),
                    guest_id=share_data.get('guest_id'),
                    amount=share_data['amount']
                )
        
        return expense

    def update(self, instance, validated_data):
        participants = validated_data.pop('participants', None)
        guest_participants = validated_data.pop('guest_participants', None)
        custom_shares = validated_data.pop('custom_shares', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if instance.split_type == 'equal':
            # Supprimer les custom shares si on passe en equal
            instance.custom_shares.all().delete()
            if participants is not None:
                instance.participants.set(participants)
            if guest_participants is not None:
                instance.guest_participants.set(guest_participants)
        else:
            # Mettre à jour les custom shares
            if custom_shares is not None:
                instance.custom_shares.all().delete()
                for share_data in custom_shares:
                    ExpenseShare.objects.create(
                        expense=instance,
                        user_id=share_data.get('user_id'),
                        guest_id=share_data.get('guest_id'),
                        amount=share_data['amount']
                    )
        
        return instance
