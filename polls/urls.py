from django.conf.urls import url,include
from polls.views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'projects', ProjectViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'process', ProcessViewSet)


urlpatterns = [
    url(r'^polls/', include(router.urls)),
    
     
]