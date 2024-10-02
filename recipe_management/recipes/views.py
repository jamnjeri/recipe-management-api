from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import Recipe, CustomUser, Category, Ingredient
from .serializers import RecipeSerializer, CustomUserSerializer, CategorySerializer, IngredientSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all() 
    serializer_class = RecipeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]               # Allow anyone to view recipes
        return [permissions.IsAuthenticated()]            # Require authentication for other actions

    def get_queryset(self):
        # If the action is to update or delete, filter by the user (Only owner can update or delete)
        if self.action in ['update', 'partial_update', 'destroy']:
            return Recipe.objects.filter(user=self.request.user)
        return super().get_queryset()  # Allow anyone to see all recipes

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
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAdminUser()]             # Only allow admin users to view the list
        return [permissions.IsAuthenticated()]             # Require authentication for other actions

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _= Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
        })

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny] 
    