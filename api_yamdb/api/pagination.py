from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class TitleCategoryGenrePagination(LimitOffsetPagination):
    """Pagination для Titles, Genres, Categories."""

    def get_paginated_response(self, data):
        if self.request.method == 'GET' and 'limit' in self.request.GET:
            return Response({
                'count': self.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data
            })
        return Response(data)
