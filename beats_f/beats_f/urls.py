from django.contrib import admin
from django.urls import include, path
from users import views # type: ignore


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('users.urls')), 
    path('admin/', admin.site.urls),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
  
    path('email/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/google/', include('users.urls')),
    
    
    path("", include("users.urls"), name="users"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)