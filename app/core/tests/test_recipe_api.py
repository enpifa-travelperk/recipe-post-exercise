from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch

from core import models, serializers

RECIPES_URL = reverse('core:recipe-list')

def get_recipe_id_url(recipe_id):
    """Return recipe detail URL"""
    return RECIPES_URL + str(recipe_id) + '/'

def create_sample_recipe(name='Allioli', description='Delicious catalan garlic mayo'):
    recipe = models.Recipe.objects.create(
        name=name,
        description=description
    )
    return recipe

def create_sample_ingredient(name='Pasta'):
    ingredient = models.Ingredient.objects.create(
        name=name
    )
    return ingredient

def get_ingredients_to_json(ingredients):
    result = []
    for ingredient in ingredients:
        result.append({"name": ingredient})
    
    return result

class RecipeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_create_recipe_without_ingredients(self):
        payload = {
            "name": "Penne carbonara",
            "description": "Super creamy and Amazing",
        }
        response = self.client.post(RECIPES_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        recipe = models.Recipe.objects.get(id=response.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_ingredients(self):
        ingredients_to_add = ['Pasta', 'Carbonara', 'Salt']
        payload = {
            "name": "Penne carbonara",
            "description": "Super creamy and Amazing",
            "ingredients": get_ingredients_to_json(ingredients_to_add)
        }

        # assert the recipe is created successfully
        response = self.client.post(RECIPES_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # assert the recipe fields contain the correct values
        recipe = models.Recipe.objects.get(id=response.data['id'])
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 3)
        for ingredient in ingredients_to_add:
            self.assertIn(ingredient, ingredients_to_add)

    def test_get_all_recipes(self):
        _ = create_sample_recipe()
        response = self.client.get(RECIPES_URL)

        recipes = models.Recipe.objects.all().order_by('-id')
        serializer = serializers.RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_get_one_recipe(self):
        recipe = create_sample_recipe()
        response = self.client.get(get_recipe_id_url(recipe.id))

        serializer = serializers.RecipeSerializer(recipe)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_ingredients(self):
        recipe_name = 'Allioli'
        recipe_description='Delicious catalan garlic mayo'
        recipe = create_sample_recipe(recipe_name, recipe_description)
        ingredients_to_add = ['Pasta', 'Pepper']
        payload = {
            "ingredients": get_ingredients_to_json(ingredients_to_add)
        }
        # assert the patch is successful
        response = self.client.patch(get_recipe_id_url(recipe.id), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert the name and description have not been updated
        # recipe.refresh_from_db() --> this would be needed if we don't do objects.get()
        recipe_db = models.Recipe.objects.get(id=recipe.id)
        # recipe_db_serializer = serializers.RecipeSerializer(recipe_db) --> can be used to verify API response
        self.assertEqual(recipe_db.name, recipe_name)
        self.assertEqual(recipe_db.description, recipe_description)

        # assert the ingredients have been added
        ingredients = recipe_db.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        for ingredient in ingredients_to_add:
            self.assertIn(ingredient, ingredients_to_add)
    
    def test_delete_recipe(self):
        # assert we have one recipe
        recipe = create_sample_recipe()
        all_recipes = models.Recipe.objects.all()
        self.assertEqual(all_recipes.count(), 1)

        # assert the recipe is deleted successfully
        response = self.client.delete(get_recipe_id_url(recipe.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # assert we have no recipes after deletion
        all_recipes = models.Recipe.objects.all()
        self.assertEqual(all_recipes.count(), 0)

