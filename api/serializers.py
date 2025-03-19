from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Document, Tag

class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""
    class Meta:
        model = Tag
        fields = ['id', 'name']

class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model"""
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Tag.objects.all(), 
        write_only=True, 
        required=False
    )
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'created', 'updated', 'tags', 'tag_ids']
        read_only_fields = ['created', 'updated']
    
    def create(self, validated_data):
        # Extract tag_ids if provided
        tag_ids = validated_data.pop('tag_ids', [])
        
        # Create document for the current user
        validated_data['user'] = self.context['request'].user
        document = Document.objects.create(**validated_data)
        
        # Add tags to the document
        if tag_ids:
            document.tags.set(tag_ids)
        
        return document
    
    def update(self, instance, validated_data):
        # Handle tag_ids if provided
        tag_ids = validated_data.pop('tag_ids', None)
        
        # Update document fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update tags if provided
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        
        return instance