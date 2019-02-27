from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from polls.serializers import ProjectSerializer, ProcessSerializer,VoteSerializer
from polls.models import Project,Process,Vote
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render
from django.db.models import Case, When
from django.http import JsonResponse
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

        return Response({'data':'Proceso de votacion abierto!'})  

    @action(methods=['get'], detail=False, permission_classes=[])
    def get_active(self, request):
        p = Process.objects.get(is_active=True)
        serializer = ProcessSerializer(p,context={'request':request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False, permission_classes=[])
    def finishProcess(self,request):
        p = Process.objects.get(is_active=True)
        serializer_class=ProjectSerializer
        winners_ids = p.finishProcess()
        keep_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(winners_ids)])
        winners = Project.objects.filter(id__in = winners_ids).order_by(keep_order)
        data = list(winners.values())
        return JsonResponse(data, safe=False) 

    @action(methods=['get'], detail=False, permission_classes=[])
    def openProcess(self,request):
        p = Process.objects.all().order_by("-id")[0]
        p.startProcess()
        
        return Response({'data':'Proceso de votacion abierto!'}) 

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class=VoteSerializer

    def list(self, request):
        queryset = Vote.objects.all()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)       

    @action(methods=['post'], detail=False, permission_classes=[])
    def add_vote(self, request):
        p = Process.objects.get(is_active=True)
        resp = p.addVote(request.user,request.data)

        return Response({'data':resp})          

       
