from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Group, GuestMember, GroupInvitation
from .serializers import GroupSerializer, UserMinimalSerializer, GuestMemberSerializer, GroupInvitationSerializer
from .export import export_group_to_csv
from .excel_export import export_group_to_excel

User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        tags=['groups'],
        summary="Liste des groupes",
        description="Retourne la liste des groupes dont l'utilisateur est membre."
    ),
    create=extend_schema(
        tags=['groups'],
        summary="Créer un groupe",
        description="Crée un nouveau groupe. L'utilisateur connecté devient automatiquement le créateur et premier membre."
    ),
    retrieve=extend_schema(
        tags=['groups'],
        summary="Détails d'un groupe",
        description="Retourne les détails complets d'un groupe avec ses membres, invités et statistiques."
    ),
    update=extend_schema(
        tags=['groups'],
        summary="Modifier un groupe",
        description="Modifie les informations d'un groupe (nom, description, devise)."
    ),
    partial_update=extend_schema(
        tags=['groups'],
        summary="Modifier partiellement un groupe",
        description="Modifie partiellement les informations d'un groupe."
    ),
    destroy=extend_schema(
        tags=['groups'],
        summary="Supprimer un groupe",
        description="Supprime définitivement un groupe. Seul le créateur peut effectuer cette action."
    ),
)
class GroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des groupes de dépenses.
    
    Un groupe permet de regrouper plusieurs personnes pour partager des dépenses.
    Chaque groupe a une devise (EUR, USD, GBP, LBP) qui s'applique à toutes ses dépenses.
    """
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

    @extend_schema(
        tags=['groups'],
        summary="Ajouter un membre",
        description="Ajoute un membre au groupe. Si l'utilisateur n'existe pas, il est ajouté comme invité.",
        request={'application/json': {'type': 'object', 'properties': {'username': {'type': 'string'}}}},
    )
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

    @extend_schema(
        tags=['export'],
        summary="Exporter en CSV",
        description="Exporte toutes les données du groupe en CSV (membres, dépenses, soldes, remboursements).",
        responses={200: OpenApiTypes.BINARY},
    )
    @action(detail=True, methods=['get'], url_path='export/csv')
    def export_csv(self, request, pk=None):
        """Exporte toutes les données du groupe en CSV"""
        group = self.get_object()
        csv_content = export_group_to_csv(group)
        
        response = HttpResponse(csv_content, content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = f'attachment; filename="fairsplit_{group.name}_{group.id}.csv"'
        
        return response

    @extend_schema(
        tags=['export'],
        summary="Exporter en Excel",
        description="Exporte toutes les données du groupe en Excel avec plusieurs feuilles (résumé, membres, dépenses, soldes, etc.).",
        responses={200: OpenApiTypes.BINARY},
    )
    @action(detail=True, methods=['get'], url_path='export/xlsx')
    def export_excel(self, request, pk=None):
        """Exporte toutes les données du groupe en Excel"""
        group = self.get_object()
        excel_file = export_group_to_excel(group)
        
        response = HttpResponse(
            excel_file.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="fairsplit_{group.name}_{group.id}.xlsx"'
        
        return response

    @extend_schema(
        tags=['invitations'],
        summary="Créer une invitation",
        description="Crée un lien d'invitation sécurisé pour rejoindre le groupe. Le lien expire après le nombre de jours spécifié.",
        request={'application/json': {
            'type': 'object',
            'properties': {
                'days_valid': {'type': 'integer', 'default': 7, 'description': 'Nombre de jours de validité'},
                'max_uses': {'type': 'integer', 'default': 0, 'description': 'Nombre maximum d\'utilisations (0 = illimité)'}
            }
        }},
    )
    @action(detail=True, methods=['post'], url_path='invitations/create')
    def create_invitation(self, request, pk=None):
        """Crée une invitation pour rejoindre le groupe"""
        group = self.get_object()
        days_valid = request.data.get('days_valid', 7)
        max_uses = request.data.get('max_uses', 0)
        
        invitation = GroupInvitation.create_invitation(
            group=group,
            days_valid=days_valid,
            max_uses=max_uses
        )
        
        serializer = GroupInvitationSerializer(invitation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        tags=['invitations'],
        summary="Liste des invitations",
        description="Retourne la liste des invitations actives du groupe.",
    )
    @action(detail=True, methods=['get'], url_path='invitations')
    def list_invitations(self, request, pk=None):
        """Liste les invitations actives du groupe"""
        group = self.get_object()
        invitations = group.invitations.filter(is_active=True)
        serializer = GroupInvitationSerializer(invitations, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=['invitations'],
    summary="Rejoindre un groupe via invitation",
    description="Permet à un utilisateur authentifié de rejoindre un groupe en utilisant un token d'invitation.",
    responses={200: GroupSerializer},
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def join_group_by_invitation(request, token):
    """Permet à un utilisateur de rejoindre un groupe via une invitation"""
    invitation = get_object_or_404(GroupInvitation, token=token)
    
    if not invitation.is_valid():
        return Response(
            {'error': 'Cette invitation n\'est plus valide'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    group = invitation.group
    user = request.user
    
    # Vérifier si l'utilisateur est déjà membre
    if group.members.filter(id=user.id).exists():
        return Response(
            {'error': 'Vous êtes déjà membre de ce groupe'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Ajouter l'utilisateur au groupe
    group.members.add(user)
    invitation.use()
    
    serializer = GroupSerializer(group)
    return Response({
        'message': f'Vous avez rejoint le groupe "{group.name}"',
        'group': serializer.data
    }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['invitations'],
    summary="Informations sur une invitation",
    description="Récupère les informations publiques d'une invitation sans rejoindre le groupe. Accessible sans authentification.",
    responses={200: GroupInvitationSerializer},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_invitation_info(request, token):
    """Récupère les informations d'une invitation (sans rejoindre)"""
    invitation = get_object_or_404(GroupInvitation, token=token)
    
    return Response({
        'group_name': invitation.group.name,
        'group_description': invitation.group.description,
        'is_valid': invitation.is_valid(),
        'expires_at': invitation.expires_at,
        'uses_count': invitation.uses_count,
        'max_uses': invitation.max_uses if invitation.max_uses > 0 else None,
    })
