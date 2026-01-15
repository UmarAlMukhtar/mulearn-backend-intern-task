from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, SkillViewSet

router = DefaultRouter()
router.register(r'listings', JobViewSet, basename='job')
router.register(r'skills', SkillViewSet, basename='skill')

urlpatterns = [
    path('', include(router.urls)),
]   