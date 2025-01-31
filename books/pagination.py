from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"  
    max_page_size = 200  

    def get_paginated_response(self, data):
        return Response(
            {
                "status": "success",
                "status": 200,
                "message": "Books retrieved successfully",
                "current_Page": self.page.number,
                "per_page": self.page_size,
                "total_pages": self.page.paginator.num_pages,
                "total_books": self.page.paginator.count,
                "data": data,
            }
        )
