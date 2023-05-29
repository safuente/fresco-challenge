"""
Database models
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password, **extra_fields):
        """Create, save and return a new user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        if not email:
            raise ValueError('User must have an email address.')
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    cook_time_minutes = models.IntegerField()
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField(
        'IngredientToRecipe'
    )
    steps = models.ManyToManyField('Step')

    def __str__(self):
        return f'{self.title}'


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Step(models.Model):
    """Step to follow for a recipe."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description


class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name




class IngredientToRecipe(models.Model):
    """Ingredient to recipe relation to manage quantities"""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)


