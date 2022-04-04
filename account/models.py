from django.db import models
import phonenumbers
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

# Function to validate Phone Numbers


def phonenumber_validator(value):
    try:
        z = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(z):
            raise ValidationError('Please enter a valid phone number')
    except Exception as e:

        if settings.DEBUG:
            raise ValidationError(str(e))
        else:
            raise ValidationError(
                'Please enter a valid phone number with international code')
    return phonenumbers.format_number(z, phonenumbers.PhoneNumberFormat.E164)


def user_profile_image_handler(instance, filename):
    return '/'.join(['documents/', "/full_image", filename])


# User Manager Class
class MyUserManager(BaseUserManager):
    def create_user(self, email, firstName, password=None, password2=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            firstName=firstName,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, password=None):
        """
        Creates and saves a superuser with the given email, firstName and password.
        """
        user = self.create_user(
            email,
            password=password,
            firstName=firstName,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Custom User Class
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100, null=True, blank=True, )
    # mobileNumber = models.CharField(
    #     max_length=50, null=True, blank=True, validators=[phonenumber_validator])
    mobileNumber = models.CharField(
        max_length=50, null=True, blank=True)
    dateOfBirth = models.DateField(null=True, blank=True, )
    gender = models.CharField(max_length=7, null=True, blank=True, )
    profilePhoto = models.ImageField(
        upload_to=user_profile_image_handler, null=True, blank=True, )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
