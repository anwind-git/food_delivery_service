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
    recipe_name = models.CharField(max_length=50, verbose_name='Название рецепта')
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
            if totals['total_kcal'] is not None:
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
        return self.recipe_name


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


def ingredients_data():
    Ingredients(name_ingredient="Шампиньоны", kcal=27, squirrels=4.30, fats=1.0, carbs=0.1).save()                    #1
    Ingredients(name_ingredient="Кабачок", kcal=24, squirrels=0.6, fats=0.3, carbs=4.6).save()                        #2
    Ingredients(name_ingredient="Картофель", kcal=76, squirrels=2.0, fats=0.4, carbs=16.10).save()                    #3
    Ingredients(name_ingredient="Морковь", kcal=32, squirrels=1.3, fats=0.1, carbs=6.9).save()                        #4
    Ingredients(name_ingredient="Лук репчатый", kcal=47, squirrels=1.4, fats=0.0, carbs=10.4).save()                  #5
    Ingredients(name_ingredient="Помидор",kcal=20, squirrels=1.1, fats=0.2, carbs=3.7).save()                         #6
    Ingredients(name_ingredient="Лук зеленый", kcal=19, squirrels=1.3, fats=0.0, carbs=4.6).save()                    #7
    Ingredients(name_ingredient="Петрушка", kcal=47, squirrels=3.7, fats=0.4, carbs=7.6).save()                       #8
    Ingredients(name_ingredient="Вода", kcal=0, squirrels=0.0, fats=0.0, carbs=0.0).save()                            #9
    Ingredients(name_ingredient="Масло подсолнечное", kcal=900, squirrels=0.0, fats=99.9, carbs=0.0).save()          #10
    Ingredients(name_ingredient="Яйцо куриное", kcal=157, squirrels=12.7, fats=10.9, carbs=0.7).save()               #11
    Ingredients(name_ingredient="Масло сливочное", kcal=748, squirrels=0.5, fats=82.5, carbs=0.8).save()             #12
    Ingredients(name_ingredient="Перец красный сладкий", kcal=27, squirrels=1.3, fats=0.0, carbs=5.3).save()         #13
    Ingredients(name_ingredient="Сыр брынза из коровьего молока", kcal=260, squirrels=17.9, fats=20.10, carbs=0.0).save()#14
    Ingredients(name_ingredient="Капуста белокочанная", kcal=27, squirrels=1.8, fats=0.1, carbs=4.7).save()          #15
    Ingredients(name_ingredient="Укроп", kcal=38, squirrels=2.5, fats=0.5, carbs=6.3).save()                         #16
    Ingredients(name_ingredient="Соль", kcal=0, squirrels=0.0, fats=0.0, carbs=0.0).save()                           #17
    Ingredients(name_ingredient="Перец черный молотый", kcal=251, squirrels=10.4, fats=3.3, carbs=38.7).save()       #18
    Ingredients(name_ingredient="Морская капуста", kcal=49, squirrels=0.8, fats=5.1, carbs=0.0).save()               #19
    Ingredients(name_ingredient="Творог 5%", kcal=121, squirrels=17.2, fats=5.0, carbs=1.8).save()                   #20
    Ingredients(name_ingredient="Малина", kcal=46, squirrels=0.8, fats=0.5, carbs=8.3).save()                        #21
    Ingredients(name_ingredient="Банан", kcal=95, squirrels=1.5, fats=0.2, carbs=21.8).save()                        #22
    Ingredients(name_ingredient="Молоко 3,2%", kcal=59, squirrels=2.90, fats=3.2, carbs=4.7).save()                  #23
    Ingredients(name_ingredient="Макароны первого сорта", kcal=335, squirrels=10.70, fats=1.3, carbs=68.40).save()   #24
    Ingredients(name_ingredient="Сахар", kcal=398, squirrels=0.0, fats=0.0, carbs=99.7).save()                       #25
    Ingredients(name_ingredient="Сухари панировочные", kcal=347, squirrels=9.70, fats=1.9, carbs=77.60).save()       #26
    Ingredients(name_ingredient="Томатная паста", kcal=80, squirrels=2.5, fats=0.3, carbs=16.7).save()               #27
    Ingredients(name_ingredient="Свекла", kcal=43, squirrels=1.5, fats=0.1, carbs=8.8).save()                        #28
    Ingredients(name_ingredient="Говядина", kcal=187, squirrels=18.9, fats=12.4, carbs=0.0).save()                   #29
    Ingredients(name_ingredient="Уксус яблочный 3%", kcal=11, squirrels=0.0, fats=0.0, carbs=2.3).save()             #30
    Ingredients(name_ingredient="Горох сушеный", kcal=298, squirrels=20.5, fats=2.0, carbs=53.3).save()              #31
    Ingredients(name_ingredient="Свинина", kcal=259, squirrels=16.0, fats=21.6, carbs=0.0).save()                    #32


def recipes_data():
    Recipes(recipe_name='Рецепт №1 Грибной суп с кабачками', serving_weight=415,
            kcal=0, squirrels=0, fats=0, carbs=0).save()
    Recipes(recipe_name='Рецепт №2 Омлет по-болгарски', serving_weight=240,
            kcal=0, fats=0, squirrels=0, carbs=0).save()
    Recipes(recipe_name='Рецепт №3 Салат из морской капусты', serving_weight=318,
            kcal=0, fats=0, squirrels=0, carbs=0).save()
    Recipes(recipe_name='Рецепт №4 Творог с ягодами', serving_weight=200,
            kcal=0, fats=0, squirrels=0, carbs=0).save()
    Recipes(recipe_name='Рецепт №5 Творожный лапшевник', serving_weight=215,
            kcal=0, fats=0, squirrels=0, carbs=0).save()
    Recipes(recipe_name='Рецепт №6 Борщ с говядиной', serving_weight=522,
            kcal=0, fats=0, squirrels=0, carbs=0).save()
    Recipes(recipe_name='Рецепт №7 Гороховый суп с мясом', serving_weight=251,
            kcal=0, fats=0, squirrels=0, carbs=0).save()


def recipe_composition():
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=1), ingredient=Ingredients.objects.get(id=1), weight=400,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=1), ingredient=Ingredients.objects.get(id=2), weight=300,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=1), ingredient=Ingredients.objects.get(id=3), weight=200,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=1), ingredient=Ingredients.objects.get(id=4), weight=100,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=1), ingredient=Ingredients.objects.get(id=5), weight=100,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=1), ingredient=Ingredients.objects.get(id=6), weight=100,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=1), ingredient=Ingredients.objects.get(id=7), weight=30,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=1), ingredient=Ingredients.objects.get(id=8), weight=20,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=1), ingredient=Ingredients.objects.get(id=9), weight=400,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=1), ingredient=Ingredients.objects.get(id=10), weight=10,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()

    AddIngredientToRecipe(recipe=Recipes.objects.get(id=2), ingredient=Ingredients.objects.get(id=11), weight=100,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=2), ingredient=Ingredients.objects.get(id=12), weight=10,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=2), ingredient=Ingredients.objects.get(id=13), weight=70,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=2), ingredient=Ingredients.objects.get(id=14), weight=60,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()

    AddIngredientToRecipe(recipe=Recipes.objects.get(id=3), ingredient=Ingredients.objects.get(id=3), weight=100,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=3), ingredient=Ingredients.objects.get(id=15), weight=50,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=3), ingredient=Ingredients.objects.get(id=5), weight=50,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=3), ingredient=Ingredients.objects.get(id=10), weight=5,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=3), ingredient=Ingredients.objects.get(id=16), weight=10,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=3), ingredient=Ingredients.objects.get(id=17), weight=2,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=3), ingredient=Ingredients.objects.get(id=18), weight=1,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=3), ingredient=Ingredients.objects.get(id=19), weight=100,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()

    AddIngredientToRecipe(recipe=Recipes.objects.get(id=4), ingredient=Ingredients.objects.get(id=20), weight=150,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=4), ingredient=Ingredients.objects.get(id=21), weight=100,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=4), ingredient=Ingredients.objects.get(id=22), weight=100,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=4), ingredient=Ingredients.objects.get(id=23), weight=50,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()

    AddIngredientToRecipe(recipe=Recipes.objects.get(id=5), ingredient=Ingredients.objects.get(id=24), weight=250,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=5), ingredient=Ingredients.objects.get(id=20), weight=250,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=5), ingredient=Ingredients.objects.get(id=11), weight=110,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=5), ingredient=Ingredients.objects.get(id=25), weight=100,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=5), ingredient=Ingredients.objects.get(id=26), weight=30,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=5), ingredient=Ingredients.objects.get(id=12), weight=20,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=5), ingredient=Ingredients.objects.get(id=17), weight=4,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()

    AddIngredientToRecipe(recipe=Recipes.objects.get(id=6), ingredient=Ingredients.objects.get(id=27), weight=60,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=6), ingredient=Ingredients.objects.get(id=15), weight=200,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=6), ingredient=Ingredients.objects.get(id=5), weight=75,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=6), ingredient=Ingredients.objects.get(id=4), weight=75,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=6), ingredient=Ingredients.objects.get(id=28), weight=250,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=6), ingredient=Ingredients.objects.get(id=9), weight=3000,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=6), ingredient=Ingredients.objects.get(id=29), weight=500,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=6), ingredient=Ingredients.objects.get(id=30), weight=15,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()

    AddIngredientToRecipe(recipe=Recipes.objects.get(id=7), ingredient=Ingredients.objects.get(id=31), weight=300,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=7), ingredient=Ingredients.objects.get(id=32), weight=500,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=7), ingredient=Ingredients.objects.get(id=9), weight=2000,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=7), ingredient=Ingredients.objects.get(id=5), weight=100,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=7), ingredient=Ingredients.objects.get(id=4), weight=90,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
    AddIngredientToRecipe(recipe=Recipes.objects.get(id=7), ingredient=Ingredients.objects.get(id=3), weight=270,
                          kcal=0, squirrels=0, fats=0, carbs=0).save()
