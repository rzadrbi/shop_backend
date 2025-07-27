from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Address, PhoneNumber
from .serializers import AddressSerializer, PhoneNumberSerializer
from .permissions import IsAdminOrSelf, IsManager

from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdminOrSelf
from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSelf]

class MyTokenObtainPairView(TokenObtainPairView):
    pass

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSelf]

    def get_queryset(self):
        # فقط آدرس‌های کاربر لاگین‌شده
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # آدرس جدید را به کاربر فعلی وصل کن
        instance = serializer.save(user=self.request.user)
        # اگر is_default=True ست شده بود، بقیه آدرس‌ها را غیرپیش‌فرض کن
        if instance.is_default:
            Address.objects.filter(user=self.request.user).exclude(pk=instance.pk).update(is_default=False)


class PhoneNumberViewSet(viewsets.ModelViewSet):
    serializer_class = PhoneNumberSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSelf]

    def get_queryset(self):
        return PhoneNumber.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        if instance.is_primary:
            PhoneNumber.objects.filter(user=self.request.user).exclude(pk=instance.pk).update(is_primary=False)
