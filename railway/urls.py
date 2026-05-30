from django.urls import path, include
from rest_framework import routers

from railway.views import StationViewSet


router = routers.DefaultRouter()
router.register("stations", StationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "railway"
