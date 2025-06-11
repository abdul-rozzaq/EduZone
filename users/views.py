from django.shortcuts import redirect
from django.contrib.auth import logout

from rest_framework import parsers, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import OTP, User, now

from .serializers import RefreshTokenSerializer, SendOTPSerializer, UserSerializer, VerifyOTPSerializer


class AuthViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(["POST"], detail=False, url_path="send-otp", url_name="send_otp")
    def send_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]

        user, created = User.objects.get_or_create(phone=phone, defaults={"is_active": False})
        otp_code = "555555"  # str(random.randint(100000, 999999))

        otp, created = OTP.objects.update_or_create(user=user, defaults={"code": otp_code, "created_at": now()})

        # send_otp_code(phone, otp_code)

        return Response({"detail": "OTP muvaffaqiyatli yuborildi."}, status=status.HTTP_200_OK)

    @action(["POST"], detail=False, url_path="verify-otp", url_name="verify_otp")
    def verify_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone, code = serializer.validated_data["phone"], serializer.validated_data["otp"]

        try:
            user = User.objects.get(phone=phone)
            otp = OTP.objects.get(user=user, code=code)

        except (User.DoesNotExist, OTP.DoesNotExist):
            return Response({"detail": "Telefon raqami yoki SMS kodi noto'g'ri."}, status=status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            return Response({"detail": "SMS kodi muddati tugagan."}, status=status.HTTP_400_BAD_REQUEST)

        otp.delete()

        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({"refresh": str(refresh), "access": str(refresh.access_token), "user": UserSerializer(instance=user, context={"request": request}).data}, status=status.HTTP_200_OK)

    @action(["POST"], detail=False, url_path="refresh-token", url_name="refresh_token")
    def refresh_token(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh_token"]

        try:
            token = RefreshToken(refresh_token)
            user = User.objects.get(id=token["user_id"])

            new_refresh_token = RefreshToken.for_user(user)
            new_access_token = new_refresh_token.access_token

            return Response(
                {"access": str(new_access_token), "refresh": str(new_refresh_token)},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({"detail": "Noto'g'ri yoki muddati tugagan token."}, status=status.HTTP_400_BAD_REQUEST)

    @action(["POST"], detail=False, url_path="sign-up", url_name="sign_up", permission_classes=[permissions.IsAuthenticated], parser_classes=[parsers.FormParser, parsers.MultiPartParser])
    def sign_up(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, instance=request.user)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(["GET"], detail=False, url_path="whoami", url_name="whoami", permission_classes=[permissions.IsAuthenticated])
    def whoami(self, request, *args, **kwargs):
        return Response(self.get_serializer(instance=request.user).data)

    def get_serializer_class(self):
        serializers = {"send_otp": SendOTPSerializer, "verify_otp": VerifyOTPSerializer, "refresh_token": RefreshTokenSerializer, "sign_up": UserSerializer}
        return serializers.get(self.action, self.serializer_class)


def logout_page(request):
    next = request.GET.get("next", "/")
    logout(request)
    return redirect(next)
