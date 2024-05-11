from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

from users.models import CustomUser


class UserManagementUtil:
    @staticmethod
    def fetch_user_details(query_params={}, id=None):
        name = query_params.get('name')
        sort_by = query_params.get('sort', 'id')
        ordered_users = None

        if id:
            all_users = CustomUser.objects.filter(id=id)
        else:
            all_users = CustomUser.objects.all()

        if name:
            all_users = all_users.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if sort_by:
            ordered_users = all_users.order_by(sort_by)
        
        return ordered_users
    
    @staticmethod
    def get_data_by_id(user_id):
        try:
            return CustomUser.objects.get(
                id=user_id
            )
        except Exception:
            return None

class CustomPaginator(PageNumberPagination):
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        try:
            return Response(
                OrderedDict(
                    [
                        ("status", data.get("status")),
                        ("message", data.get("message")),
                        ("page", self.page.number),
                        ("total_count", self.page.paginator.count),
                        ("page_size", self.get_page_size(self.request)),
                        ("next", self.get_next_link()),
                        ("previous", self.get_previous_link()),
                        ("data", data.get("data"))
                    ]
                )
            )
        except Exception:
            return Response(
                OrderedDict(
                    [
                        ("status", data.get("status")),
                        ("message", data.get("message")),
                        ("page", None),
                        ("total_count", None),
                        ("page_size", None),
                        ("next", None),
                        ("previous", None),
                        ("data", data.get("data"))
                    ]
                )
            )        
