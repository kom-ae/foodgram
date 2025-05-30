# Generated by Django 4.2.20 on 2025-05-13 16:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipes.models
import validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=64, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[validators.validate_amount], verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredientmodel', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'рецепт-ингредиент',
                'verbose_name_plural': 'Рецепты-Ингредиенты',
                'default_related_name': 'recipesingredients',
            },
        ),
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(default=None, max_length=32, null=True, unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='RecipeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='Название')),
                ('image', models.ImageField(upload_to='recipes/images/')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Время приготовления не может быть меньше 1 минуты.')], verbose_name='Время приготовления (в минутах)')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации.')),
                ('short_link', models.CharField(default=recipes.models.get_uuid, editable=False, max_length=7, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(through='recipes.RecipeIngredientModel', to='recipes.ingredientmodel', verbose_name='Ингредиенты')),
                ('tags', models.ManyToManyField(to='recipes.tagmodel', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
                'default_related_name': 'recipes',
            },
        ),
        migrations.AddField(
            model_name='recipeingredientmodel',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipemodel', verbose_name='Рецепт'),
        ),
        migrations.AddConstraint(
            model_name='ingredientmodel',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='Unique Ingredient-measurement_unit constraint'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredientmodel',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='Unique recipe-ingredient constraint'),
        ),
    ]
