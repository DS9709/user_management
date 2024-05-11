import logging

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from users.serializers import UserSerializer
from users.utils import UserManagementUtil, CustomPaginator

logger = logging.getLogger(__name__)

class UserView(APIView):
    def get(self, request, id=None):
        query_params = request.query_params
        limit = query_params.get("limit", 5)
        paginator = CustomPaginator()
        paginator.page_size = limit

        try:
            ordered_users = UserManagementUtil.fetch_user_details(query_params=query_params, id=id)
            if not ordered_users:
                raise NotFound()

            ordered_users = paginator.paginate_queryset(ordered_users, request)
            response_data = UserSerializer(ordered_users, many=True).data
            paginated_response = paginator.get_paginated_response(
                {
                    "data": response_data,
                    "status": status.HTTP_200_OK,
                    "message": "success"
                }
            )
        except NotFound:
            logger.info(f"No user found for given request combination")
            paginated_response = paginator.get_paginated_response(
                {
                    "status": status.HTTP_204_NO_CONTENT,
                    "data": {},
                    "message": "No user found for given request combination"
                }
            )
        except Exception as e:
            logger.info(f"Error: {e} occured while trying to fetch user records.")
            paginated_response = paginator.get_paginated_response(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "data": {},
                    "message": "Could not fetch user records."
                }
            )

        return paginated_response

    def post(self, request, id=None):
        request_data = request.data
        serializer = UserSerializer(data=request_data)

        if not serializer.is_valid():
            return Response(
                {
                    "status": "error",
                    "data": {},
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        first_name = validated_data["first_name"]
        user_id = validated_data["id"]
        serializer.save()

        return Response(
            {
                "status": "success",
                "data": {},
                "message": f"New user {first_name} created with user_id: {user_id}"
            },
            status=status.HTTP_201_CREATED
        )
    
    def put(self, request, id=None):
        if not id:
            return Response(
                {
                    "status": "error",
                    "data": {},
                    "message": "id value not passed in the url"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        _data = request.data
        user_data = UserManagementUtil.get_data_by_id(user_id=id)
        if not user_data:
            return Response(
                {
                    "status": "error",
                    "data": {},
                    "message": f"Passed value of id: {id} in the url is incorrect."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        for key, value in _data.items():
            if hasattr(user_data, key):
                setattr(user_data, key, value)
        
        user_data.save()
        return Response(
            {
                "status": "success",
                "data": {},
                "message": f"Details updated for user_id: {id}"
            },
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, id=None):
        if not id:
            return Response(
                {
                    "status": "error",
                    "data": {},
                    "message": "id value not passed in the url"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        _data = request.data
        user_data = UserManagementUtil.get_data_by_id(user_id=id)
        if not user_data:
            return Response(
                {
                    "status": "error",
                    "data": {},
                    "message": f"Passed value of id: {id} in the url is incorrect."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user_data.delete()
        return Response(
            {
                "status": "success",
                "data": {},
                "message": f"user_id: {id} successfully deleted"
            },
            status=status.HTTP_200_OK
        )