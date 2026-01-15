from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Job
from .serializers import JobSerializer
from .permissions import IsAdminUserRole, IsCompanyUserRole, IsOwnerOrReadOnly

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    
    # Filtering and Searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'company', 'job_type', 'location', 'skills__name']
    search_fields = ['title', 'description']

    def get_permissions(self):
        """Assign permissions based on the action (list, create, etc.)"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [IsCompanyUserRole | IsAdminUserRole]
        elif self.action in ['verify', 'reject']:
            permission_classes = [IsAdminUserRole]
        else: # update, partial_update, destroy
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Combined logic for Soft Delete and Role-Based Access."""
        user = self.request.user
        
        # Rule 0: NEVER show soft-deleted items
        base_query = Job.objects.filter(is_deleted=False)

        # 1. ADMIN: Sees all non-deleted jobs
        if user.is_authenticated and user.role == 'admin':
            return base_query
            
        # 2. COMPANY: Sees all verified jobs + their own pending/draft jobs
        if user.is_authenticated and user.role == 'company':
            return base_query.filter(Q(status='verified') | Q(company=user))
            
        # 3. PUBLIC: Sees only verified jobs
        return base_query.filter(status='verified')

    def perform_create(self, serializer):
        """Automatically set the company to the logged-in user."""
        serializer.save(company=self.request.user)

    def perform_destroy(self, instance):
        """Soft delete: mark as deleted instead of removing from DB."""
        instance.is_deleted = True
        instance.save()

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        job = self.get_object()
        job.status = 'verified'
        job.save()
        return Response({'status': 'job verified successfully'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        job = self.get_object()
        job.status = 'rejected'
        job.save()
        return Response({'status': 'job rejected'})