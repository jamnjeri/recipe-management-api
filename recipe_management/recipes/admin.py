from django.contrib import admin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'date_joined', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('date_joined',)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email', 'date_joined')  # Add more fields as necessary

admin.site.register(CustomUser, CustomUserAdmin)
