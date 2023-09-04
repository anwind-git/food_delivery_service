from django.contrib import admin
from .models import Ingredients, Recipes, AddIngredientToRecipe


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ['name_ingredient', 'kcal', 'squirrels', 'fats', 'carbs']
    search_fields = ['name_ingredient']
    list_per_page = 15


@admin.register(Recipes)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['recipe_name', 'serving_weight', 'kcal', 'squirrels', 'fats', 'carbs']
    search_fields = ['recipe_name']
    list_per_page = 15


@admin.register(AddIngredientToRecipe)
class AddIngredientToRecipeAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'weight']
    list_filter = ['recipe']
    list_per_page = 15

