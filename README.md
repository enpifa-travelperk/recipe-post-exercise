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
