from django.urls import path
from .views import BookListView, BookDetailView, home

urlpatterns = [
    path("", home),
    path('api/v1/books/', BookListView.as_view(), name='book-list'),
    path('api/v1/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]
