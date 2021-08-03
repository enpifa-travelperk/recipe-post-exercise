from rest_framework import serializers

from core.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for an ingredient object"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    # What is the difference between this commented call and the next call
    # and why do we use this variable for?

    # ingredients = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Ingredient.objects.all(),
    #     allow_null=True,
    #     required=False
    # )
    ingredients = IngredientSerializer(
        many=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'description', 'ingredients'
        )
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        """
        Create a new recipe initially without the ingredients, 
        then add the ingredients one by one and create the PK-FK relationship.
        - validated_data contains the payload from the POST request.
        
        POST payload example on 'recipes/':
        {
            "name": "Penne carbonara",
            "description": "Super creamy and Amazing",
            "ingredients": [
                {"name": "Pasta"},
                {"name": "Carbonara sauce"}
            ]
        }
        """
        ingredients_payload = validated_data.pop('ingredients', [])

        # new_recipe will not have the ingredients initially
        new_recipe = Recipe.objects.create(**validated_data)

        # add the PK-FK relationship for all the ingredients-recipe
        for ingredient in ingredients_payload:
            Ingredient.objects.create(recipe=new_recipe, **ingredient)

        return new_recipe
    
    def update(self, instance, validated_data):
        """
        Update the list of ingredients for a recipe.
        - validated_data contains the payload from the PATCH request

        PATCH payload example on '/recipes/1/':
        {
            "name": "Penne carbonara",
            "description": "Super creamy and Amazing",
            "ingredients": [
                {"name": "Fusili"},
                {"name": "Carbonara sauce"},
                {"name": "Pepper"}
            ]
        }
        """
        new_ingredients = validated_data.pop('ingredients', [])

        # How do we get the recipe without updating the rest of the fields (name, description)?
        recipe = super().update(instance, validated_data)
        Ingredient.objects.filter(recipe=recipe).delete()

        for ingredient in new_ingredients:
            Ingredient.objects.create(recipe=recipe, **ingredient)

        return recipe
