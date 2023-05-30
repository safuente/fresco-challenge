from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient

from recipes.serializers import RecipeSerializer


RECIPES_URL = reverse('recipes:recipe-list')


def detail_url(recipe_id):
    """Create and return a recipe detail URL."""
    return reverse('recipes:recipe-detail', args=[recipe_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def create_ingredient(**params):
    """Create and return a sample ingredient."""
    defaults = {
        'name': 'test_ingredient',
    }

    defaults.update(params)

    ingredient = Ingredient.objects.create(**defaults)
    return ingredient


def create_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults = {
            'title': 'test_recipe',
            'description': 'test_description',
            'cook_time_minutes': 10
        }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)
        self.ingredient = create_ingredient(name="test_ingredient_1")
        self.payload = {
            'title': 'test_recipe',
            'description': 'test_description',
            'cook_time_minutes': 10,
            'tags': [
                {
                    'name': 'test_tag_1'
                }
            ],
            'ingredients': [
                {
                    'ingredient': 1,
                    'quantity': '10',
                    'unit': 'g'
                }
            ],
            'steps': [
                {
                    'name': 'test_step_1',
                    'description': 'test_description_1'
                }
            ]
        }

    def test_create_recipe(self):
        """Test creating a recipe."""

        res = self.client.post(RECIPES_URL, self.payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data.get('id'))
        serializer = RecipeSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(recipe.user, self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        create_recipe(user=self.user)
        create_recipe(user=other_user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
