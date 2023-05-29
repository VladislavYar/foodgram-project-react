from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    """Переименовывает поле для ограничения вывода."""
    page_size_query_param = 'limit'
