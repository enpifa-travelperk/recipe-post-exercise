# Django training exercise - Recipe
Create a CRUD API with Django and DRF that allows you to CRUD recipes and add/delete ingredients to it.  Test it using postman or similar.
Create automated tests for every action similar to https://slides.com/israelsaetaperez/test-driven-development/#/5/1.

Recipe: Name, Description
Ingredient: Name, Recipe (ForeignKey) ← assume a given ingredient belongs only to one recipe, even if that means multiple Ingredient instances with the exact same name.

## Versions used

Django version: 2.1.latest
DRF version: 3.9.latest

## Start django project in Docker

run `docker-compose run app sh -c "django-admin startproject app ."`
it starts a new project called `app` in the current directory

## Create a core directory where to store the core files of our project

run `docker-compose run app sh -c "python manage.py startapp core"`

## Make migrations everytime we update the model / database

run `docker-compose run app sh -c "python manage.py makemigrations core"`
run `docker-compose run app sh -c "python manage.py migrate"`

## Add postgresql

Do corresponding updates to requirements, Dockerfile and docker-compose to add the packages to install and set up the configurations, then run `docker-compose build`

## CONCERNS

To create a recipe associated to one or more ingredients, I can try:
{
  "name": "Penne carbonara",
  "description": "Super creamy and Amazing",
  "ingredients": [3]
}

"ingredients" is expecting a list of primary keys
However, we don't have ingredients. We should create some.

We can't create new ingredients on the browser because the new ingredients need to be associated to a recipe, but we can't set it with the current viewer.

If I try with the VS extension, we can try something like:
{
  "name": "salsasita",
  "recipe_id": 3
}
but this throws a 500 internal server error...
```Exception Value: null value in column "recipe_id" violates not-null constraint
DETAIL:  Failing row contains (9, salsasita, null).```

I'm not sure if I can create an ingredient that I can add later on when creating recipes.

`/api/recipes/` is not showing the recipes once created, but `/api/recipes/1/` is showing the recipe with id 1

when updating a recipe with new ingredients, the new ingredients are created and shown on `/api/ingredients/` but the tests don't show them
