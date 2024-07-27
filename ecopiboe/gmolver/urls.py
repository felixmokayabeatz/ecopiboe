from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_gmolver, name='menu_gmolver'),
    path('upload/', views.upload_file, name='upload_file'),
    # path('screns_gmolver/', views.screns_gmolver, name='screns_gmolver'),
]
