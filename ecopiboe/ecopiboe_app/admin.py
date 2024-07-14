from django.contrib import admin
from .models import Userinfo
from .models import ChatBot
from .models import EcoFootprintCategory
from .models import EcoFootprintQuestion
from .models import AIResult
from .models import UserResponse



admin.site.register(Userinfo)
admin.site.register(ChatBot)
admin.site.register(EcoFootprintCategory)
admin.site.register(EcoFootprintQuestion)
admin.site.register(AIResult)
admin.site.register(UserResponse)


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


from django import forms
from .models import BlogPost

class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = User.objects.filter(is_staff=True)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm