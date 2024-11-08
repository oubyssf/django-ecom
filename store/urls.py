from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.update_user, name='update_user'),
    path('profile-info/', views.update_user_info, name='update_user_info'),
    path('update-password/', views.update_password, name='update_password'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<slug:slug>', views.category, name='category'),
    path('categories/', views.categories, name='categories'),
    path('search/', views.search, name='search'),
]