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
    def create_user(self, email, first_name, password=None, password2=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def update_user(self, **kwargs):
    #     user = self.model(
    #         email=self.normalize_email(kwargs['email']),
    #         first_name=kwargs['first_name'],
    #         last_name=kwargs['last_name'],
    #         mobile_number=kwargs['mobile_number'],
    #         date_of_birth=kwargs['date_of_birth'],
    #         gender=kwargs['gender'],
    #         profile_photo=kwargs['profile_photo'],
    #     )

    #     user.set_password(kwargs['password'])
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, email, first_name, password=None):
        """
        Creates and saves a superuser with the given email, first_name and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True, )
    mobile_number = models.CharField(
        max_length=50, null=True, blank=True, validators=[phonenumber_validator])
    date_of_birth = models.DateField(null=True, blank=True, )
    gender = models.CharField(max_length=7, null=True, blank=True, )
    profile_photo = models.ImageField(
        upload_to=user_profile_image_handler, null=True, blank=True, )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

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
