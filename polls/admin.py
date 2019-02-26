from django.contrib import admin
from .models import Process,Project,Vote

class ProcessAdmin(admin.ModelAdmin):
    list_display=('is_active',)
    
admin.site.register(Process,ProcessAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display=('name','value')
    
admin.site.register(Project,ProjectAdmin)

class VoteAdmin(admin.ModelAdmin):
    list_display= ('get_owner','get_process')
    def get_owner(self, obj):
        return obj.user.email
    def get_process(self, obj):
        return obj.process.quarter
admin.site.register(Vote,VoteAdmin)
