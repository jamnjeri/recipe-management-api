from rest_framework import serializers
from .models import CustomUser, Recipe, Category, Ingredient, RecipeIngredient
from django.contrib.auth import get_user_model

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'date_joined']
        read_only_fields = ['date_joined']

    def create(self, validated_data):
        # Create a user with the provided data
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']

    def validate(self, data):
        # Check if ingredient data is provided
        if 'ingredient' not in data or not data['ingredient'].get('name'):
            raise serializers.ValidationError({"ingredient": "Ingredient name is required."})

        # Check if quantity is provided
        if 'quantity' not in data or not data['quantity']:
            raise serializers.ValidationError({"quantity": "Quantity is required."})

        return data

class RecipeSerializer(serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'instructions', 'preparation_time', 'cooking_time', 'servings', 'created_date', 'recipe_ingredients', 'categories', 'image']
        
    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError("Image is required")
        return value
    
    def validate(self, data):
        if 'recipe_ingredients' not in data or not data['recipe_ingredients']:
            raise serializers.ValidationError({"recipe_ingredients": "At least one ingredient is required."})

        return data

    def create(self, validated_data):
        recipe_ingredients_data = validated_data.pop('recipe_ingredients')
        categories_data = validated_data.pop('categories')
        recipe = Recipe.objects.create(**validated_data)

        # Handle recipe ingredients
        for recipe_ingredient_data in recipe_ingredients_data:
            ingredient_data = recipe_ingredient_data.pop('ingredient')

            if not ingredient_data.get('name'):
                raise serializers.ValidationError({"ingredient": "Ingredient name is required."})
            
            ingredient, _= Ingredient.objects.get_or_create(name=ingredient_data['name'])
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, **recipe_ingredient_data)

        # Handle categories
        for category_data in categories_data:
            category_obj, _ = Category.objects.get_or_create(name=category_data['name'])
            recipe.categories.add(category_obj)
        
        return recipe
        
    def update(self, instance, validated_data):
        receipe_ingredients_data = validated_data.pop('recipe_ingredients', None)
        categories_data = validated_data.pop('categories', None)

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.instructions = validated_data.get('instructions', instance.instructions)
        instance.preparation_time = validated_data.get('preparation_time', instance.preparation_time)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.servings = validated_data.get('servings', instance.servings)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        # Update recipe ingredients if present
        if receipe_ingredients_data is not None:
            instance.recipe_ingredients.all().delete()
            for recipe_ingredient_data in receipe_ingredients_data:
                ingredient_data = recipe_ingredient_data.pop('ingredient')
                ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_data['name'])
                RecipeIngredient.objects.create(recipe=instance, ingredient=ingredient, **recipe_ingredient_data)

        # Update categories if present
        if categories_data is not None:
            instance.categories.clear()
            for category_data in categories_data:
                category_obj,_=Category.objects.get_or_create(name=category_data['name'])
                instance.categories.add(category_obj)

        return instance
