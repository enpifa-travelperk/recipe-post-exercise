from django.db import models
from django.conf import settings


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    # TODO: Is blank, default necessary?
    name = models.CharField(max_length=255, blank=False, default=None)
    recipe = models.ForeignKey(
        settings.RECIPE_MODEL,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    name = models.CharField(max_length=255, blank=False, default=None)
    description = models.CharField(max_length=255, blank=False, default=None)
    # ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name