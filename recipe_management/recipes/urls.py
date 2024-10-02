from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, CategoryViewSet, IngredientViewSet, CustomUserViewSet, CustomAuthToken, UserRegisterView

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)