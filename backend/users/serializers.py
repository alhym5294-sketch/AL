from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import FaceProfile, FaceSample, User


class FaceSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceSample
        # embedding is biometric material: writable, never exposed on read.
        fields = ['id', 'embedding', 'pose', 'quality_score', 'source', 'captured_at']
        read_only_fields = ['id', 'captured_at']
        extra_kwargs = {'embedding': {'write_only': True}}


class FaceProfileSerializer(serializers.ModelSerializer):
    person_name = serializers.CharField(source='person.name', read_only=True)
    sample_count = serializers.SerializerMethodField()
    samples = FaceSampleSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = FaceProfile
        fields = ['id', 'person', 'person_name', 'version', 'model_name',
                  'model_version', 'is_verified', 'sample_count', 'samples',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'version', 'created_at', 'updated_at']

    def get_sample_count(self, obj):
        # prefetch_related('samples') in the viewset keeps this to one pass.
        return obj.samples.count()

    def create(self, validated_data):
        samples = validated_data.pop('samples', [])
        profile = super().create(validated_data)
        FaceSample.objects.bulk_create(
            FaceSample(profile=profile, **sample) for sample in samples)
        return profile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False,
                                     validators=[validate_password])
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'user_type', 'user_type_display',
                  'code', 'email', 'phone', 'department', 'subject', 'stage', 'branch',
                  'is_active', 'is_superuser', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'is_superuser': {'required': False},
            'username': {'required': True},
            'name': {'required': True},
            'user_type': {'required': True},
        }

    def _set_password(self, user, raw_password):
        if raw_password:
            user.set_password(raw_password)
        return user

    def create(self, validated_data):
        raw_password = validated_data.pop('password', '')
        if not raw_password:
            raise serializers.ValidationError({'password': 'كلمة المرور مطلوبة.'})
        user = User(**validated_data)
        self._set_password(user, raw_password)
        user.save()
        return user

    def update(self, instance, validated_data):
        raw_password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if raw_password:
            self._set_password(instance, raw_password)
        instance.save()
        return instance

    def validate_code(self, value):
        if value:
            qs = User.objects.filter(code=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError('هذا الرقم مستخدم مسبقاً.')
        return value
