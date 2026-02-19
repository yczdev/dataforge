from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Schema

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class SchemaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Schema
        fields = ["id", "owner", "name", "definition", "row_count", "created_at", "updated_at"]

    def validate_definition(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Definition must be a list of field definitions")
        for item in value:
            if not isinstance(item, dict):
                raise serializers.ValidationError("Each definition item must be an object")
            if "field_name" not in item or "data_type" not in item:
                raise serializers.ValidationError("Each item must include 'field_name' and 'data_type'")
            if not item["field_name"] or not isinstance(item["field_name"], str):
                raise serializers.ValidationError("'field_name' must be a non-empty string")
            if not item["data_type"] or not isinstance(item["data_type"], str):
                raise serializers.ValidationError("'data_type' must be a non-empty string")
        return value