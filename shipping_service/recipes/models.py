"""
Модуль моделей Django в службе доставки еды для представления рецептов и их состава.
"""
from django.db import models
from django.db.models import Sum, CharField


class Ingredients(models.Model):
    """
    Модель, представляющая ингредиенты для составления рецепта.
    """
    name_ingredient = models.CharField(max_length=30, verbose_name='Наименование')
    kcal = models.IntegerField(verbose_name='Калорийность на 100г')
    fats = models.FloatField(verbose_name='Жиры на 100г')
    squirrels = models.FloatField(verbose_name='Белки на 100г')
    carbs = models.FloatField(verbose_name='Углеводы на 100г')

    def save(self, *args, **kwargs):
        """
        Переопределенный метод сохранения для обновления связанных рецептов.
        """
        super().save(*args, **kwargs)
        recipes_composition = AddIngredientToRecipe.objects.all()
        recipes = Recipes.objects.all()
        for item_composition in recipes_composition:
            if item_composition.ingredient.id == self.pk:
                item_composition.save()
        for item_recipes in recipes:
            if item_recipes.needed_for_dishes.exists() and item_recipes.needed_for_dishes.filter(id=self.pk).exists():
                item_recipes.save()

    class Meta:
        """
        Метаданные для модели ингредиентов.
        """
        db_table = 'ingredients'
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name_ingredient']

    def __str__(self) -> CharField:
        """
        Возвращает строковое представление ингредиентов.
        """
        return self.name_ingredient


class Recipes(models.Model):
    """
    Модель, представляющая рецепт и вес порции.
    """
    recipe_name = models.CharField(max_length=50, verbose_name='Название рецепта')
    serving_weight = models.IntegerField(verbose_name='Вес порции грамм')
    needed_for_dishes = models.ManyToManyField('Ingredients',
                                               through='AddIngredientToRecipe')
    kcal = models.FloatField(editable=False, verbose_name='Калорийность')
    fats = models.FloatField(editable=False, verbose_name='Жиры')
    squirrels = models.FloatField(editable=False, verbose_name='Белки')
    carbs = models.FloatField(editable=False, verbose_name='Углеводы')

    def save(self, *args, **kwargs):
        """
        Переопределенный метод сохранения для вычисления пищевой ценности рецепта.
        """
        if self.id is not None:
            totals = AddIngredientToRecipe.objects.filter(recipe=self.id).aggregate(
                total_kcal=Sum('kcal'),
                total_weight=Sum('weight'),
                total_fats=Sum('fats'),
                total_squirrels=Sum('squirrels'),
                total_carbs=Sum('carbs'),
            )
            if totals['total_kcal'] is not None:
                self.kcal = round(totals['total_kcal'] * self.serving_weight /
                                  totals['total_weight'], 2)
                self.fats = round(totals['total_fats'] * self.serving_weight /
                                  totals['total_weight'], 2)
                self.squirrels = round(totals['total_squirrels'] * self.serving_weight /
                                       totals['total_weight'], 2)
                self.carbs = round(totals['total_carbs'] * self.serving_weight /
                                   totals['total_weight'], 2)
        else:
            self.kcal = 0
            self.fats = 0
            self.squirrels = 0
            self.carbs = 0
        super().save(*args, **kwargs)

    class Meta:
        """
        Метаданные для модели рецептов.
        """
        db_table = 'recipes'
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> CharField:
        """
        Возвращает строковое представление рецепта.
        """
        return self.recipe_name


class AddIngredientToRecipe(models.Model):
    """
    Модель, представляющая состава рецепта.
    """
    recipe = models.ForeignKey('Recipes', on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey('Ingredients', on_delete=models.CASCADE,
                                   verbose_name='Ингредиент')
    weight = models.IntegerField(verbose_name='Вес ингредиента грамм')
    kcal = models.FloatField(editable=False, verbose_name='Калорийность')
    fats = models.FloatField(editable=False, verbose_name='Жиры')
    squirrels = models.FloatField(editable=False, verbose_name='Белки')
    carbs = models.FloatField(editable=False, verbose_name='Углеводы')

    def save(self, *args, **kwargs):
        """
        Переопределенный метод сохранения для вычисления кжбу.
        """
        self.kcal = (self.ingredient.kcal / 100) * float(self.weight)
        self.fats = (self.ingredient.fats / 100) * float(self.weight)
        self.squirrels = (self.ingredient.squirrels / 100) * float(self.weight)
        self.carbs = (self.ingredient.carbs / 100) * float(self.weight)

        super().save(*args, **kwargs)
        recipes = Recipes.objects.filter(needed_for_dishes__id=self.pk)
        for item_recipes in recipes:
            item_recipes.save()

    class Meta:
        """
        Метаданные для модели состава рецепта.
        """
        db_table = 'add_ingredient_to_recipe'
        verbose_name = 'рецепт и ингредиент'
        verbose_name_plural = 'Состав рецептов'
        ordering = ['-id']

    def __str__(self) -> str:
        """
        Возвращает строковое представление состава рецепта.
        """
        return str(self.recipe)
