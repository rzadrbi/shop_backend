from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Q, UniqueConstraint

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'کاربر ساده'),
        ('manager', 'مدیر'),
        ('accountant', 'حسابدار'),
        ('warehouse', 'انباردار'),
        ('vip', 'کاربر ویژه'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        help_text='نقش کاربر در سیستم'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Address(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    label        = models.CharField(max_length=50, default='Home')
    line1        = models.CharField(max_length=255)
    line2        = models.CharField(max_length=255, blank=True)
    city         = models.CharField(max_length=100)
    postal_code  = models.CharField(max_length=20)
    country      = models.CharField(max_length=50, default='Iran')
    is_default   = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user'], condition=Q(is_default=True),
                name='unique_default_address_per_user'
            )
        ]
        ordering = ['-is_default', 'label']

    def __str__(self):
        return f"{self.user.username} – {self.label}"


class PhoneNumber(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='phones')
    number       = PhoneNumberField(unique=True, blank=True, null=True)
    is_primary   = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} – {self.number}"

