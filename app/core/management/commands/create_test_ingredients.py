"""
Django command to create test ingredients in the database.
"""
from django.core.management.base import BaseCommand
from core.models import Ingredient


class Command(BaseCommand):
    """Django command to create test ingredients."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        ingredient_name = 'test_ingredient_'
        for el in list(range(1, 11)):
            Ingredient.objects.create(name=f'{ingredient_name}_{el}')
