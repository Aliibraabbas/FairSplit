from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Group, GuestMember, GroupInvitation

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class GuestMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestMember
        fields = ['id', 'name']


class GroupSerializer(serializers.ModelSerializer):
    members = UserMinimalSerializer(many=True, read_only=True)
    created_by = UserMinimalSerializer(read_only=True)
    guest_members = GuestMemberSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    currency_symbol = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'currency', 'currency_symbol', 'members', 'guest_members', 'created_by', 'member_count', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        return obj.members.count() + obj.guest_members.count()
    
    def get_currency_symbol(self, obj):
        return obj.get_currency_symbol()


class GroupInvitationSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = GroupInvitation
        fields = ['id', 'group', 'group_name', 'token', 'created_at', 'expires_at', 'max_uses', 'uses_count', 'is_active', 'is_valid']
        read_only_fields = ['token', 'created_at', 'uses_count']

    def get_is_valid(self, obj):
        return obj.is_valid()
