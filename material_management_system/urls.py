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
    path('', views.material_search, name="material_search"),
    path('new_item/', views.new_item, name="new_item"),
    path('update_item/<str:pk>/', views.update_item, name="update_item"),
    path('delete_item/<str:pk>/', views.delete_item, name="delete_item"),
    path('new_material/<str:pk>/', views.new_material, name="new_material"),
    path('remaining_material', views.remaining_material, name="remaining_material"),
    path('item_detail/<str:pk>/', views.item_detail, name="item_detail"),
    path('update_material', views.update_material, name="update_material"),
    path('project_search', views.project_search, name="project_search"),
    path('new_project', views.new_project, name="new_project"),
    path('new_bom', views.new_bom, name="new_bom"),
]