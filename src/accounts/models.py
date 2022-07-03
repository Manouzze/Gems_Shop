from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.

class CustomAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):

        if not email:
            raise ValueError('Vous devez entrer un email 🤦🏻‍♀️')

        if not username:
            raise ValueError("Vous devez entrer un nom d'utilisateur 🤦🏻‍♀️")

        user = self.model(
                username = username,
                email = self.normalize_email(email),
            )

        user.set_password(password) #Pour ne pas stocker le password en clair dans la base de db
        user.save(using=self._db)
        return user



    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password=password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class CustomAccount(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255, blank=False)
    username = models.CharField(max_length=150, blank=True)

    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superadmin        = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = CustomAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True



class UserProfile(models.Model):
    user = models.OneToOneField(CustomAccount, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.user.username

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'