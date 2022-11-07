from rest_framework.pagination import LimitOffsetPagination

class LimitOffset8Pagination(LimitOffsetPagination):
    default_limit = 8

class LimitOffset16Pagination(LimitOffsetPagination):
    default_limit = 4