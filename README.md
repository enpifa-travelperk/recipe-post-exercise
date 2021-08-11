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

`/api/recipes/` is not showing the recipes once created, but `/api/recipes/1/` is showing the recipe with id 1 (this happens in the browser)

when updating a recipe with new ingredients, the new ingredients are created and shown on `/api/ingredients/` but the tests don't show them
also not only the ingredients are updated, but also the name and description
