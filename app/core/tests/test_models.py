from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from core import models


def create_sample_recipe():
    recipe = models.Recipe.objects.create(
        name='Allioli',
        description='Delicious catalan garlic mayo'
    )
    return recipe


class ModelTests(TestCase):
    def test_recipe_str(self):
        "Test the recipe string representation"
        recipe = create_sample_recipe()

        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        recipe = create_sample_recipe()
        ingredient = models.Ingredient.objects.create(
            name='Cucumber',
            recipe=recipe
        )

        self.assertEqual(str(ingredient), ingredient.name)
