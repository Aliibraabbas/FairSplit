from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from groups.models import Group
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group = get_object_or_404(Group, id=self.kwargs['group_pk'], members=self.request.user)
        return Expense.objects.filter(group=group)

    def perform_create(self, serializer):
        group = get_object_or_404(Group, id=self.kwargs['group_pk'], members=self.request.user)
        serializer.save(group=group, created_by=self.request.user)
