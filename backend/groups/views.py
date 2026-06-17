from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Group, GuestMember
from .serializers import GroupSerializer, UserMinimalSerializer, GuestMemberSerializer

User = get_user_model()


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        group = serializer.save(created_by=self.request.user)
        group.members.add(self.request.user)

    def destroy(self, request, *args, **kwargs):
        group = self.get_object()
        if group.created_by != request.user:
            return Response(
                {'error': 'Seul le créateur peut supprimer ce groupe'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='members/add')
    def add_member(self, request, pk=None):
        group = self.get_object()
        username = request.data.get('username', '').strip()
        if not username:
            return Response({'error': 'Nom requis'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            group.members.add(user)
            return Response({'type': 'registered', **UserMinimalSerializer(user).data})
        except User.DoesNotExist:
            guest, created = GuestMember.objects.get_or_create(group=group, name=username)
            if not created:
                return Response({'error': f'"{username}" est déjà dans le groupe'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'type': 'guest', **GuestMemberSerializer(guest).data}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='members/remove')
    def remove_member(self, request, pk=None):
        group = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            if user == group.created_by:
                return Response(
                    {'error': 'Impossible de supprimer le créateur du groupe'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            group.members.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='guests/remove')
    def remove_guest(self, request, pk=None):
        group = self.get_object()
        guest_id = request.data.get('guest_id')
        try:
            guest = GuestMember.objects.get(id=guest_id, group=group)
            guest.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except GuestMember.DoesNotExist:
            return Response({'error': 'Invité non trouvé'}, status=status.HTTP_404_NOT_FOUND)
