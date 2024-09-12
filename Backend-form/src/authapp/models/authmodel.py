from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager,AbstractUser,Group, Permission


class CustomUserManager(UserManager):
    def _create_user(self, email=None, password=None, **extra_fields):

        if not email:
            return "email must be set"
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('is_active', True)
        
        user = self._create_user(email, password, **extra_fields)

        try:
            admin_group = Group.objects.get(id=1)
            user.groups.add(admin_group)
        except Group.DoesNotExist:
            pass
        
        return user


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=True, default="")
    phone_no = models.CharField(max_length=30 ,null=True,blank=True, default="")
    first_name = models.CharField(max_length=50, null=True, blank=True, default="")
    last_name = models.CharField(max_length=50, null=True, blank=True, default="")
    street_address = models.CharField(max_length=255, null=True, blank=True, default="")
    state = models.CharField(max_length=255, null=True, blank=True, default="")
    city = models.CharField(max_length=255, null=True, blank=True, default="")
    postal_code = models.CharField(max_length=100, null=True, blank=True, default="")
    country = models.CharField(max_length=255, null=True, blank=True, default="")
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_provideradmin = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'  # Unique related_name for groups field
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'  # Unique related_name for user_permissions field
    )


    
    

