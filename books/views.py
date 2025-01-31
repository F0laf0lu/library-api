from rest_framework import status, generics, response
from django_ratelimit.decorators import ratelimit
from .models import Book
from .serializers import BookSerializer
from django.http import HttpResponse
from rest_framework.throttling import AnonRateThrottle


def home(request):
    return HttpResponse("Welcome to Library Management API. Go to api/v1/books ")


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer



class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response.Response(
            {
                "status": "success",
                "code": 200,
                "message": "Book details retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(
            {
                "status": "success",
                "code": 200,
                "message": "Book updated successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(
            {"status": "success", "message": "Book deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
