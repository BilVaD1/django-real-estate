from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User

class UserAdmin(BaseUserAdmin):
    ordering = ['email'] # задает порядок сортировки в административном интерфейсе по электронной почте.
    add_form = CustomUserCreationForm # add_form и form - это формы, используемые для создания и изменения пользователя соответственно.
    form = CustomUserChangeForm
    model = User
    list_display = ['pkid', 'id', 'email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_display_links = ['id', 'email']
    list_filter = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active']
    # определяет, какие поля будут отображаться и группироваться в административном интерфейсе редактирования пользователя.
    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": ("email", "password", )
            },
        ),
        (
            _("Personal Information"),
            {"fields":("username", "first_name", "last_name",)}
        ),
        (
            _("Permissions and Groups"),
            {
                "fields":(
                "is_active", 
                "is_staff", 
                "is_superuser",
                "groups", 
                "user_permissions",
                )
            },
        ),
        (
            _("Important Dates"), {"fields": ("last_login", "date_joined")}
        ),
    )
    # определяет, какие поля будут отображаться при создании нового пользователя.
    add_fieldsets=(
            (None,{
                "classes": ("wide",), # "classes": ("wide",) в определении add_fieldsets является настройкой стилей для административной формы Django. Это указывает, что форма должна быть широкой, что может быть полезным, например, для обеспечения лучшей видимости полей при создании пользователя.
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            }
        )
    )
    search_fields = ["email", "username", "first_name", "last_name"]

admin.site.register(User, UserAdmin)