from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'description',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_name(self, value):
        instance = self.instance
        if Category.objects.filter(name=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError('Já existe uma categoria com este nome.')
        return value