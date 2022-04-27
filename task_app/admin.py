from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Task, Team

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    """
        Created CustomUserAdmin for rendering required 
        field through the Admin Page
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'role', 'is_staff']

    def get_fieldsets(self, request, obj=None):
        fs = super(CustomUserAdmin, self).get_fieldsets(request, obj)
        fs += (
            ('Role', {
                'fields': ('role','email'),
                'description': 'set Role and Email',
            }),
        )
        return fs


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Task)
admin.site.register(Team)
