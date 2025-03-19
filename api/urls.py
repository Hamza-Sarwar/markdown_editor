from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, TagViewSet, UserLoginView

# Create router
router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'users', UserLoginView, basename='user')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
]