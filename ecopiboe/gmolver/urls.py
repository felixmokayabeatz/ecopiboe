from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_gmolver, name='menu_gmolver'),
    path('file_analyser/', views.fileanalyser, name='fileanalyser'),
    # path('screns_gmolver/', views.screns_gmolver, name='screns_gmolver'),
]
