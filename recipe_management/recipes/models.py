from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

# Create your models here.
# Users
class CustomUser(AbstractUser):
    email = models. EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

        # Add unique related_name attributes
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change to avoid clash
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Change to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser'
    )

    def __str__(self):
        return self.username

# Category
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Ingredient
class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # quantity = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Recipe
class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField()
    preparation_time = models.IntegerField()
    cooking_time = models.IntegerField()
    servings = models.IntegerField()
    image_url = models.URLField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredient_recipes')
    categories = models.ManyToManyField(Category, related_name='category_recipes')
    image = models.ImageField(upload_to='recipe/images', default='recipes/images/No-Food-Image.png', null=False, blank=False )

    def __str__(self):
        return self.title
    
# Junction table for Recipe and Ingredient
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity} of {self.ingredient}: {self.recipe}"