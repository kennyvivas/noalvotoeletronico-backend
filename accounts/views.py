from django.shortcuts import render
import uuid
from rest_framework import views, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

class UserLogoutAllView(views.APIView):
    """
    Use this endpoint to log out all sessions for a given user.
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        user.jwt_secret = uuid.uuid4()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserGetRole(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user=request.user
        return Response(user.is_admin)   