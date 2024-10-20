from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, filters
from .models import Recipe, CustomUser, Category, Ingredient
from .serializers import RecipeSerializer, CustomUserSerializer, CategorySerializer, IngredientSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .permissions import IsRecipeOwner
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all() 
    serializer_class = RecipeSerializer

    # Enable Search Filter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'title',
        'categories__name',
        'recipe_ingredients__ingredient__name',
        'preparation_time',
    ]
    ordering_fields = [
        'created_date',
        'preparation_time',
        'cooking_time',
        'servings',
    ]
    ordering = ['-created_date']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]               # Allow anyone to view recipes
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsRecipeOwner()]
        return [permissions.IsAuthenticated()]            # Require authentication for other actions

    def get_queryset(self):
        queryset = Recipe.objects.all()

        # Filter by category if the 'category' query param is provided
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(categories__id=category_id).distinct()

        # Filter by ingredient if the 'ingredient' query param is provided
        ingredient_name = self.request.query_params.get('ingredient', None)
        if ingredient_name is not None:
            queryset = queryset.filter(recipe_ingredients__ingredient__name__icontains=ingredient_name).distinct()

        # Filter by cooking time, servings, or preparation time
        cooking_time = self.request.query_params.get('cooking_time', None)
        if cooking_time is not None:
            queryset = queryset.filter(cooking_time=cooking_time)

        servings = self.request.query_params.get('servings', None)
        if servings is not None:
            queryset = queryset.filter(servings=servings)

        preparation_time = self.request.query_params.get('preparation_time', None)
        if preparation_time is not None:
            queryset = queryset.filter(preparation_time=preparation_time)

        # If the action is to update or delete, filter by the user (Only owner can update or delete)
        if self.action in ['update', 'partial_update', 'destroy']:
            return Recipe.objects.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        # Set the user to the currently authenticated user
        print("Request User:", self.request.user)
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return super().get_queryset()

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all() 
    serializer_class = IngredientSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return super().get_queryset()

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAdminUser()]             # Only allow admin users to view the list
        return [permissions.IsAuthenticated()]             # Require authentication for other actions

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            raise Response({'error': 'Username and password are required'}, status=400)

        user = authenticate(username=username, password=password)

        if user is None:
            # Check if user exists
            if CustomUser.objects.filter(username=username).exists():
                return Response({'error': 'Incorrect password'}, status=400)
            else:
                return Response({'error': 'User not found'}, status=400)
            
        # If user is authenticated, get or create the token
        try:
            token, created = Token.objects.get_or_create(user=user)
        except IntegrityError as e:
            # Handle any issues that occur during token creation
            return Response({'error': 'Error creating token'}, status=500)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
        })
class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny] 
    