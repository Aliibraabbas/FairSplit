from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from groups.models import Group, GuestMember
from accounts.serializers import UserSerializer
from groups.serializers import GuestMemberSerializer
from .models import Reimbursement
from .services import calculate_balances, calculate_settlements

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_balances(request, group_pk):
    group = get_object_or_404(Group, id=group_pk, members=request.user)
    user_balances, guest_balances = calculate_balances(group)
    return Response({
        'members': [
            {'user': UserSerializer(b['user']).data, 'balance': b['balance']}
            for b in user_balances
        ],
        'guests': [
            {'guest': GuestMemberSerializer(b['guest']).data, 'balance': b['balance']}
            for b in guest_balances
        ],
    })


def _serialize_party(party):
    if party['type'] == 'guest':
        return {'type': 'guest', 'id': party['obj'].id, 'name': party['obj'].name}
    return {'type': 'user', 'id': party['obj'].id, 'name': party['obj'].username}


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_settlements(request, group_pk):
    group = get_object_or_404(Group, id=group_pk, members=request.user)
    settlements = calculate_settlements(group)
    return Response([
        {
            'from': _serialize_party(s['from']),
            'to': _serialize_party(s['to']),
            'amount': s['amount'],
        }
        for s in settlements
    ])


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_reimbursement(request, group_pk):
    group = get_object_or_404(Group, id=group_pk, members=request.user)
    from_type = request.data.get('from_type')
    from_id = request.data.get('from_id')
    to_id = request.data.get('to_id')
    amount = request.data.get('amount')

    to_user = get_object_or_404(User, id=to_id)

    r = Reimbursement(group=group, to_user=to_user, amount=amount)
    if from_type == 'guest':
        r.from_guest = get_object_or_404(GuestMember, id=from_id, group=group)
    else:
        r.from_user = get_object_or_404(User, id=from_id)
    r.save()
    return Response({'id': r.id}, status=status.HTTP_201_CREATED)
