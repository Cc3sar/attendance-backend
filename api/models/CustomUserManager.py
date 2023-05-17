from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    """
        Custom superuser manager
    """

    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        """
            Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            **extra_fields
        )
        
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
            Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user