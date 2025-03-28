from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("please enter a valid email"))

    def create_user(self, email, first_name, last_name, company, password, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        
        else:
            raise ValueError("The Email field must be set")
        user = self.model(email=email, first_name=first_name, last_name=last_name, company=company, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, company, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is staff must be true for admin user"))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is superuser must be true for admin user"))
        
        user = self.create_user(email, first_name, last_name, company, password, **extra_fields)
        user.save(using=self._db)
        return user