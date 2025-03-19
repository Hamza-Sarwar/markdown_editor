from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Document, Tag
from .serializers import DocumentSerializer, TagSerializer

class UserLoginView(viewsets.ViewSet):
    """
    View for user login using JWT
    """
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Invalid Credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

class DocumentViewSet(viewsets.ModelViewSet):
    """
    Viewset for Document CRUD operations
    """
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only return documents for the logged-in user
        queryset = Document.objects.filter(user=self.request.user)
        
        # Filter by tag if tag_id is provided
        tag_id = self.request.query_params.get('tag_id')
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        
        # Sorting options
        sort_by = self.request.query_params.get('sort_by')
        if sort_by == 'created':
            queryset = queryset.order_by('created')
        elif sort_by == '-created':
            queryset = queryset.order_by('-created')
        elif sort_by == 'updated':
            queryset = queryset.order_by('updated')
        elif sort_by == '-updated':
            queryset = queryset.order_by('-updated')
        
        return queryset

class TagViewSet(viewsets.ModelViewSet):
    """
    Viewset for Tag CRUD operations
    """
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tag.objects.all()