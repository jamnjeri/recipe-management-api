from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

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
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredient_recipes')
    categories = models.ManyToManyField(Category, related_name='category_recipes')

    def __str__(self):
        return self.title