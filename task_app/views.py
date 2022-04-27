from functools import partial
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer,UserSerializer, TeamSerializer
from .models import *

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permisssions import IsUserPermission, IsLeaderOrMemberPermission
from .task import send_email_to_team_leader

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': 403, 'payload': serializer.errors})
        serializer.save()

        user = CustomUser.objects.get(username = serializer.data['username'])
        token_obj, _ = Token.objects.get_or_create(user = user)
        return Response({'status': 200, 'payload': serializer.data, 'token': str(token_obj)})



class TeamListCreateView(generics.ListCreateAPIView):
    """
        role = User will be able to Create and List all the Team in Database
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsUserPermission]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    """
        role = User will be able to Create and List all the Task in Database
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsUserPermission]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save()
        team_id = serializer.data['team']
        task_name = serializer.data['name']
        from_email = self.request.user.email
        send_email_to_team_leader(team_id, from_email, task_name)


class TaskUpdateView(generics.UpdateAPIView):
    """
        Only Team Leader Or Team Member can update the Task's object
        and Member will be able to update status field only
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsLeaderOrMemberPermission]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def update(self, request, *args, **kwargs):
        # if current user is a Team Member, then he should be able to update
        # status field only, hence I'm using partial = True in Serializier
        if request.user.role == 'M':
            instance = self.get_object()
            serializer = self.get_serializer(instance, data={'status': request.data.get("status")}, partial=True)
            serializer.is_valid()
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return super().update(request, *args, **kwargs)