from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Group, GuestMember

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

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'members', 'guest_members', 'created_by', 'member_count', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        return obj.members.count() + obj.guest_members.count()
