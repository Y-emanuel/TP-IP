from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index-page'),
    path('registration/login/', views.user_login, name='login'),  # Apuntar a views.user_login
    path('home/', views.home, name='home'),
    path('buscar/', views.search, name='buscar'),
    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),
    path('exit/', views.exit, name='exit'),
