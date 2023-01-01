from django.urls import include, path
from reactions.views import ReactionCompoundViewSet, ReactionViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"reaction_compound", ReactionCompoundViewSet)
router.register(r"reaction", ReactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
