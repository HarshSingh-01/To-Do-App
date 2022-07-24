from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("<int:id>", views.toDoList, name="toDoList"),
    path('create/', views.create, name='create'),
    path('view/', views.view, name="view"),
]
