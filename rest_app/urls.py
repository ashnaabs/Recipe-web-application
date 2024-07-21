from django.urls import path
from rest_app import views
from . views import *

urlpatterns=[
    path('create/',RecipeCreativeView.as_view(),name='create'),
    path('details/<int:pk>',RecipesDetails.as_view(),name='details'),
    path('update/<int:pk>',RecipesUpdateView.as_view(),name='update'),
    path('delete/<int:pk>',RecipesDelete.as_view(),name='delete'),
    path('search/<str:Name>',RecipeSearch.as_view(),name='search'),   #searching a recipe by giving the name in url

    path('create_recipe/<int:id>',views.CreateRecipe,name='create_recipe'),
path('create_recipe/', views.CreateRecipe, name='create_recipe'),
    path('recipe_fetch/<int:id>/',views.recipe_fetch,name='recipe_fetch'),
    path('update_recipe/<int:id>/',views.update_recipe,name='update_recipe'),
    path('recipe_delete/<int:id>/',views.recipe_delete,name='recipe_delete'),
    path('',views.index,name='index'),
    path('update_detail/<int:id>/',views.update_detail,name='update_detail'),
]