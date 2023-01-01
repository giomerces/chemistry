from compounds.views import CompoundStoreViewSet, CompoundViewSet, StoreViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"compound", CompoundViewSet)
router.register(r"store", StoreViewSet)
router.register(r"compound_store", CompoundStoreViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
