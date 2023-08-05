from django.db import models


class Ingredients(models.Model):
    name_ingredient = models.CharField(max_length=30, verbose_name='Наименование')
    kcal = models.IntegerField(verbose_name='Калорийность на 100г')
    fats = models.FloatField(verbose_name='Жиры на 100г')
    squirrels = models.FloatField(verbose_name='Белки на 100г')
    carbs = models.FloatField(verbose_name='Углеводы на 100г')

    class Meta:
        db_table = 'ingredients'
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name_ingredient


class Recipes(models.Model):
    recipe = models.CharField(max_length=50, verbose_name='Название рецепта')
    serving_weight = models.IntegerField(verbose_name='Вес порции грамм')
    needed_for_dishes = models.ManyToManyField('Ingredients', through='AddIngredientToRecipe')

    class Meta:
        db_table = 'recipes'
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.recipe


class AddIngredientToRecipe(models.Model):
    recipe = models.ForeignKey('Recipes', on_delete=models.CASCADE, verbose_name='Рецепт')
    ingredient = models.ForeignKey('Ingredients', on_delete=models.CASCADE, verbose_name='Ингредиент')
    weight = models.IntegerField(verbose_name='Вес ингредиента грамм')
    kcal = models.FloatField(editable=False, verbose_name='Калорийность')
    fats = models.FloatField(editable=False, verbose_name='Жиры')
    squirrels = models.FloatField(editable=False, verbose_name='Белки')
    carbs = models.FloatField(editable=False, verbose_name='Углеводы')

    def save(self, *args, **kwargs):
        self.kcal = (self.ingredient.kcal / 100) * self.weight
        self.fats = (self.ingredient.fats / 100) * self.weight
        self.squirrels = (self.ingredient.squirrels / 100) * self.weight
        self.carbs = (self.ingredient.carbs / 100) * self.weight
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'add_ingredient_to_recipe'
        verbose_name = 'рецепт и ингридиент'
        verbose_name_plural = 'Состав рецептов'

    def __str__(self):
        return str(self.recipe)