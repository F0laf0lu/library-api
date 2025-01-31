from rest_framework import status, generics
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer




class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



