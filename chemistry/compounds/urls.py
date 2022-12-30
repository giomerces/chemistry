from compounds.views import CompoundViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", CompoundViewSet)

# Wire up our API using automatic URL routing.
# Additionally, login URLs included for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
]
