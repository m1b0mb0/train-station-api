from rest_framework import mixins, viewsets
from django.db.models import Count, Prefetch

from railway.models import (
    Station,
    Route,
    TrainType,
    Train,
    Journey,
    Crew
)
from railway.serializers import (
    StationSerializer,
    RouteSerializer,
    RouteListSerializer,
    TrainTypeSerializer,
    TrainSerializer,
    TrainListSerializer,
    JourneySerializer,
    JourneyListSerializer,
    JourneyRetrieveSerializer,
    CrewSerializer,
    CrewListSerializer,
    CrewRetrieveSerializer
)


class StationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = RouteListSerializer

        return serializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.select_related("source", "destination")

        return queryset


class TrainTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = TrainListSerializer

        return serializer

    def get_queryset(self):
        train_type = self.request.query_params.get("train_type")

        queryset = self.queryset

        if train_type:
            queryset = queryset.filter(
                train_type__name__icontains=train_type
            )

        if self.action == "list":
            queryset = queryset.select_related("train_type")

        return queryset


class JourneyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = JourneyListSerializer

        if self.action == "retrieve":
            serializer = JourneyRetrieveSerializer

        return serializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related(
                "route",
                "route__source",
                "route__destination",
                "train",
            )

        if self.action == "retrieve":
            queryset = queryset.select_related("train__train_type")

        return queryset


class CrewViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = CrewListSerializer

        if self.action in "retrieve":
            serializer = CrewRetrieveSerializer

        return serializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.annotate(journeys_count=Count("journeys"))

        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                Prefetch(
                    "journeys",
                    queryset=Journey.objects.select_related(
                        "route",
                        "route__source",
                        "route__destination",
                        "train"
                    )
                )
            )

        return queryset
