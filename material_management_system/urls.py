"""material_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.material_search, name="material_search"),
    path('material_detail_search/', views.material_detail_search, name="material_detail_search"),
    path('materials_price/', views.materials_price, name="materials_price"),
    path('new_item/', views.new_item, name="new_item"),
    path('update_item/<str:pk>/', views.update_item, name="update_item"),
    path('delete_item/<str:pk>/', views.delete_item, name="delete_item"),
    path('new_material/<str:pk>/', views.new_material, name="new_material"),
    path('remaining_material', views.remaining_material, name="remaining_material"),
    path('item_detail/<str:pk>/', views.item_detail, name="item_detail"),
    path('update_material/<str:pk>/', views.update_material, name="update_material"),
    path('delete_material/<str:pk>/', views.delete_material, name="delete_material"),
    path('project_search', views.project_search, name="project_search"),
    path('new_project', views.new_project, name="new_project"),
    path('project_detail/<str:pk>/', views.project_detail, name="project_detail"),
    path('update_project/<str:pk>/', views.update_project, name="update_project"),
    path('delete_project/<str:pk>/', views.delete_project, name="delete_project"),
    path('new_bom/<str:pk>/', views.new_bom, name="new_bom"),
    path('bom_detail/<str:pk>/', views.bom_detail, name="bom_detail"),
    path('bom_back/<str:pk>/', views.bom_back, name="bom_back"),
    path('return_material/<str:pk1>/<str:pk2>/', views.return_material, name="return_material"),
    path('return_material_update/<str:pk1>/<str:pk2>/', views.return_material_update, name="return_material_update"),

]
