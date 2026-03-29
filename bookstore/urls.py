from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/n1/', views.books_n1, name='books_n1'),
    path('books/optimized/', views.books_optimized, name='books_optimized'),
    path('explain/', views.explain, name='explain'),
]
