from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job
from .serializers import JobSerializer
from .permissions import IsAdminUserRole, IsCompanyUserRole, IsOwnerOrReadOnly

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer

    def get_permissions(self):
        """Assign permissions based on the action (list, create, etc.)"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [IsCompanyUserRole | IsAdminUserRole]
        else: # update, partial_update, destroy
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        
        # 1. Admins see EVERYTHING
        if user.is_authenticated and user.role == 'admin':
            return Job.objects.all()
            
        # 2. Companies see ALL verified jobs + THEIR OWN pending/draft jobs
        if user.is_authenticated and user.role == 'company':
            from django.db.models import Q
            return Job.objects.filter(Q(status='verified') | Q(company=user))
            
        # 3. Public/Students see ONLY verified jobs
        return Job.objects.filter(status='verified')

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)
        
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserRole])
    def verify(self, request, pk=None):
        job = self.get_object()
        job.status = 'verified'
        job.save()
        return Response({'status': 'job verified successfully'})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserRole])
    def reject(self, request, pk=None):
        job = self.get_object()
        job.status = 'rejected' # You might need to add 'rejected' to your STATUS_CHOICES
        job.save()
        return Response({'status': 'job rejected'})
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'company', 'job_type', 'location', 'skills__name']
    search_fields = ['title', 'description']