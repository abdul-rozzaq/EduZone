from rest_framework import serializers

from .models import User


class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "birthday",
            "region",
            "district",
            "score",
            "balance",
            "study_time",
            "is_active",
        ]
        read_only_fields = ["is_active", "score", "balance", "study_time", "phone"]
