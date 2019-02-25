from rest_framework import serializers
from polls.models import Project,Process,Vote

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields=('id','name','description','value')


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields=('id','quarter','total_budget','is_active','winner_list')        

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields=('user','process','votes')     