from rest_framework import status, generics, response
from django_ratelimit.decorators import ratelimit
from .models import Book
from .serializers import BookSerializer
from django.http import HttpResponse
from rest_framework.throttling import AnonRateThrottle
from .throttles import BookAnonRateThrottle, BookUserRateThrottle
import time

def get_rate_limit_headers(view, request):
    """Retrieve rate-limit headers from the applied throttle classes."""
    headers = {}
    for throttle in view.get_throttles():
        if hasattr(throttle, "get_cache_key"):
            throttle_key = throttle.get_cache_key(request, view)
            if not throttle_key:
                continue

            rate = throttle.get_rate()
            if not rate:
                continue

            num_requests, duration_unit = rate.split("/")
            num_requests = int(num_requests)

            duration_map = {"sec": 1, "min": 60, "hour": 3600, "day": 86400}
            duration = duration_map.get(duration_unit, 60)

            history = throttle.cache.get(throttle_key, [])
            remaining = max(num_requests - len(history), 0)
            reset_time = int(history[0] + duration) if history else int(time.time())

            headers.update(
                {
                    "X-RateLimit-Limit": str(num_requests),
                    "X-RateLimit-Remaining": str(remaining),
                    "X-RateLimit-Reset": str(reset_time),
                }
            )
    return headers


def home(request):
    return HttpResponse("Welcome to Library Management API. Go to api/v1/books ")


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        headers = get_rate_limit_headers(self, request)
        response["headers"] = headers
        response.data["headers"] = headers
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        headers = get_rate_limit_headers(self, request)
        response["headers"] = headers
        response.data["headers"] = headers
        return response


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance) 
        headers = get_rate_limit_headers(self, request)
        return response.Response(
            {
                "status": "success",
                "code": 200,
                "message": "Book details retrieved successfully",
                "data": serializer.data,
                "headers":  headers
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        headers = get_rate_limit_headers(self, request)
        self.perform_update(serializer)
        return response.Response(
            {
                "status": "success",
                "code": 200,
                "message": "Book updated successfully",
                "data": serializer.data,
                "header":headers
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        headers = get_rate_limit_headers(self, request)
        return response.Response(
            {"status": "success", "message": "Book deleted successfully", "header":headers},
            status=status.HTTP_204_NO_CONTENT,
        )
