from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_custom_pagination_data(self):
        return {
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'total_items': self.page.paginator.count,
                'items_per_page': self.page.paginator.per_page,
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous()
            }