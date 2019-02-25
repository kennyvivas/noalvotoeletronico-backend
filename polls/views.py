from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from polls.serializers import ProjectSerializer, ProcessSerializer,VoteSerializer
from polls.models import Project,Process,Vote
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render
import json

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class=ProjectSerializer

    def list(self, request):
        queryset = Project.objects.all()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

    @action(methods=['get'], detail=False, permission_classes=[])
    def get_projects(self, request):
        queryset = Project.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)        

class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class=ProcessSerializer

    def list(self, request):
        queryset = Process.objects.all()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)  

    @action(methods=['get'], detail=True, permission_classes=[])
    def init_process(self, request,pk=None):
        p = Process.objects.get(id=pk)
        p.startProcess()

        return Response({'data':'Voting process is open'})  

    @action(methods=['get'], detail=False, permission_classes=[])
    def get_active(self, request):
        p = Process.objects.get(is_active=True)
        # serializer = self.serializer_class(queryset, many=True)
        serializer = ProcessSerializer(p,context={'request':request})
        return Response(serializer.data)
        

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class=VoteSerializer

    def list(self, request):
        queryset = Vote.objects.all()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)       

    @action(methods=['post'], detail=True, permission_classes=[])
    def add_vote(self, request,pk=None):
        p = Process.objects.get(id=pk)
        p.addVote(json.dumps(request.data['vote']))

        return Response({'data':'Vote accepted'})          

       
