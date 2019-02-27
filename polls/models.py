from django.db import models
from django.shortcuts import get_object_or_404

from accounts.models import User
import json

class Project(models.Model):
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=255,null=True, blank=True)
    value = models.IntegerField()
    def __str__(self):
        return self.name

class Process(models.Model):
    QUARTERS = (
        ('1', 'January / March'),
        ('2', 'April / June'),
        ('3', 'July / September'),
        ('4', 'October / December'),
    )
    # Recordar que el modelo no es con un usuario, es con todos los registrados
    quarter = models.CharField(max_length=1,choices=QUARTERS,default='1')
    voters = models.ManyToManyField(User,null=True, blank=True)
    options = models.ManyToManyField(Project,null=True, blank=True)
    is_active = models.BooleanField(default="False") 
    total_budget = models.IntegerField()
    remaining_budget = models.IntegerField(null=True, blank=True)
    vote_list = models.CharField(max_length=255,null=True, blank=True)
    winner_list = models.CharField(max_length=255,null=True, blank=True)
    voters_list = models.CharField(max_length=255,null=True, blank=True)

    def addVote(self,user, new_votes_list):  
        p = Process.objects.get(is_active=True)
        check_if_voted = len(Vote.objects.filter(user=user,process=p))
        
        # if check_if_voted<1:
        if type(self.vote_list) is str:
            vote_list = json.loads(self.vote_list)
            for currentVote in vote_list:
                for newVote in  new_votes_list:
                    if newVote["id"] == currentVote["id"]:
                        currentVote["value"] += newVote["value"]
            self.vote_list = json.dumps(vote_list)
        else:
            self.vote_list = json.dumps(new_votes_list)
        vote = Vote()
        vote.user=user
        vote.process = p
        vote.save();             
        self.save()
        return('Tu voto ha sido aceptado')    
        # else:
        #     return('Ya has votado en este proceso')            

    def topVotes(self):
        vote_list = json.loads(self.vote_list)
        return sorted(vote_list,key=lambda x: x["value"],reverse=True)

    
    def startProcess(self):
        self.is_active = True
        self.save()

    def finishProcess(self):
        final_list = Process.topVotes(self)
        print(final_list)
        self.remaining_budget = self.total_budget
        winner_list = []
        winner_list_names = []
        vote_list = final_list

        for option in vote_list:
            project=get_object_or_404(Project,pk=option['id'])
            s = self.remaining_budget - project.value
            if ( s >= 0):
                winner_list.append(project.id)
                temp = project.name + " | "+str(project.value)
                winner_list_names.append( temp)
                self.remaining_budget = s
            
        self.winner_list = winner_list
        self.is_active = False
        self.save()
        return(self.winner_list)
            
class Vote(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    process = models.ForeignKey(Process,on_delete=models.CASCADE)
    votes=models.CharField(max_length=255,null=True, blank=True)


             






        
        


