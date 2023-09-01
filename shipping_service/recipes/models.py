from django.db import models
from django.db.models import Sum


# ингредиенты для составления рецепта
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


# рецепт и вес порции
class Recipes(models.Model):
    recipe = models.CharField(max_length=50, verbose_name='Название рецепта')
    serving_weight = models.IntegerField(verbose_name='Вес порции грамм')
    needed_for_dishes = models.ManyToManyField('Ingredients', through='AddIngredientToRecipe')
    kcal = models.FloatField(editable=False, verbose_name='Калорийность')
    fats = models.FloatField(editable=False, verbose_name='Жиры')
    squirrels = models.FloatField(editable=False, verbose_name='Белки')
    carbs = models.FloatField(editable=False, verbose_name='Углеводы')

    def save(self, *args, **kwargs):
        # вычисления итоговой пищевой ценности рецепта
        if self.id is not None:
            totals = AddIngredientToRecipe.objects.filter(recipe=self.id).aggregate(
                total_kcal=Sum('kcal'),
                total_weight=Sum('weight'),
                total_fats=Sum('fats'),
                total_squirrels=Sum('squirrels'),
                total_carbs=Sum('carbs'),
            )
            self.kcal = round(totals['total_kcal'] * self.serving_weight / totals['total_weight'], 2)
            self.fats = round(totals['total_fats'] * self.serving_weight / totals['total_weight'], 2)
            self.squirrels = round(totals['total_squirrels'] * self.serving_weight / totals['total_weight'], 2)
            self.carbs = round(totals['total_carbs'] * self.serving_weight / totals['total_weight'], 2)
        else:
            self.kcal = 0
            self.fats = 0
            self.squirrels = 0
            self.carbs = 0
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'recipes'
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.recipe


# состав рецепта
class AddIngredientToRecipe(models.Model):
    recipe = models.ForeignKey('Recipes', on_delete=models.CASCADE, verbose_name='Рецепт')
    ingredient = models.ForeignKey('Ingredients', on_delete=models.CASCADE, verbose_name='Ингредиент')
    weight = models.IntegerField(verbose_name='Вес ингредиента грамм')
    kcal = models.FloatField(editable=False, verbose_name='Калорийность')
    fats = models.FloatField(editable=False, verbose_name='Жиры')
    squirrels = models.FloatField(editable=False, verbose_name='Белки')
    carbs = models.FloatField(editable=False, verbose_name='Углеводы')

    # вычисляем кжбу по формуле: (калорийность / 100) * вес и т.д.
    def save(self, *args, **kwargs):
        self.kcal = (self.ingredient.kcal / 100) * float(self.weight)
        self.fats = (self.ingredient.fats / 100) * float(self.weight)
        self.squirrels = (self.ingredient.squirrels / 100) * float(self.weight)
        self.carbs = (self.ingredient.carbs / 100) * float(self.weight)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'add_ingredient_to_recipe'
        verbose_name = 'рецепт и ингредиент'
        verbose_name_plural = 'Состав рецептов'

    def __str__(self):
        return str(self.recipe)
