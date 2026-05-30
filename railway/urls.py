from django.urls import path, include
from rest_framework import routers

from railway.views import (
    StationViewSet,
    RouteViewSet,
    TrainTypeViewSet,
    TrainViewSet,
    JourneyViewSet,
    CrewViewSet
)


router = routers.DefaultRouter()
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("train_types", TrainTypeViewSet)
router.register("trains", TrainViewSet)
router.register("journeys", JourneyViewSet)
router.register("crews", CrewViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "railway"
