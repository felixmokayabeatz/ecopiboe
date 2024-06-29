from django.contrib import admin
from .models import Userinfo
from .models import ChatBot
from .models import EcoFootprintCategory
from .models import EcoFootprintQuestion
from .models import AIResult



admin.site.register(Userinfo)
admin.site.register(ChatBot)
admin.site.register(EcoFootprintCategory)
admin.site.register(EcoFootprintQuestion)
admin.site.register(AIResult)


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

