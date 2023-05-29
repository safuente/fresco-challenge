"""
Serializers for recipe APIs
"""
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from core.models import (
    Recipe,
    Tag,
    Ingredient,
    Step,
    IngredientToRecipe
)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ['name']


class IngredientToRecipeSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = IngredientToRecipe
        fields = ['id', 'ingredient', 'quantity', 'unit']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class StepSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Step
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientToRecipeSerializer(many=True, required=False)
    steps = StepSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'cook_time_minutes', 'tags',
            'ingredients', 'steps'
        ]
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_steps(self, steps, recipe):
        """Handle getting or creating steps as needed."""
        for step in steps:
            step_obj, created = Step.objects.get_or_create(
                **step,
            )
            recipe.steps.add(step_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handle getting or creating ingredients as needed."""
        print(ingredients)
        for i, ingredient in enumerate(ingredients):
            ingredient_obj, created = IngredientToRecipe.objects.get_or_create(
                **ingredient,
            )
            print(ingredient_obj)
            print(created)
            # IngredientToRecipe.objects.create(recipe=recipe, ingredient=ingredient['ingredient'], quantity=ingredient['quantity'], unit=ingredient['unit'])
            recipe.ingredients.add(ingredient_obj)
            # ingredients_to_recipe = IngredientToRecipe.objects.create(ingredient=ingredient_obj,  recipe=recipe, quantity=ingredient.quantity, unit=ingredient.unit)
            # recipe.ingredients.add(ingredients_to_recipe)

    def create(self, validated_data):
        """Create a recipe."""
        print(validated_data)
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        steps = validated_data.pop('steps', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_steps(steps, recipe)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        steps = validated_data.pop('steps', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if steps is not None:
            instance.steps.clear()
            self._get_or_create_steps(steps, instance)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
