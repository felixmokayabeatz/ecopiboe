from django.contrib import admin
from django.urls import include, path
from ecopiboe_app import views # type: ignore


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('ecopiboe_app.urls')), 
    path('admin/', admin.site.urls),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
  
    path('email/', include('ecopiboe_app.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/google/', include('ecopiboe_app.urls')),
    path('tinymce/', include('tinymce.urls')),
    
    
    path("", include("ecopiboe_app.urls"), name="ecopiboe_app"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)