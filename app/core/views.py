from rest_framework import viewsets, mixins, status

from core.models import Ingredient, Recipe
from core import serializers

class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Retrieve the recipes that match 'name' from url"""
        recipes_name = self.request.query_params.get('name')
        queryset = self.queryset
        if recipes_name:
            queryset = queryset.filter(name__exact=recipes_name)

        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        return self.serializer_class
    
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save()
    