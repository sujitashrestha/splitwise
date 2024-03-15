from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name,middle_name, phone_no, role, password=None, password2=None):
        """
        Creates and saves a User with the given email, phone_no, terms_and_condition, role, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must provide a first name')
        if not middle_name:
            raise ValueError('Users must provide a middle name')
        if not last_name:
            raise ValueError('Users must provide a last name')
        if not role:
            raise ValueError('Users must assign a role for creating user.')
        
        

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name = last_name,
            phone_no=phone_no,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role, first_name, middle_name, last_name, phone_no, password=None):
        """
        Creates and saves a superuser with the given first_name, middle_name, last_name,
        email, role, phone_no.
        """
        user = self.create_user(
            email,
            password=password,
            role=role,
            first_name = first_name,
            middle_name= middle_name,
            last_name = last_name,
            phone_no=phone_no
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

USER_ROLES = (
    ("Admin","Admin"),
    ("User","User"),

)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # Custom fields ------------------------------------------------
    first_name = models.CharField(max_length=128,null=True,blank=True)
    middle_name = models.CharField(max_length=128,null=True,blank=True)
    last_name = models.CharField(max_length=128,null=True,blank=True)
    phone_no = models.CharField(max_length=10)
    role = models.CharField(choices=USER_ROLES, max_length=121, default='Farmer')
    is_email_verified = models.BooleanField(default=False)

    # --------------------------------------------------------------

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["role","first_name","middle_name","last_name"]

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserTokens(models.Model):
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    interests = models.CharField(max_length=255, blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

