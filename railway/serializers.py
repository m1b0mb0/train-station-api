from rest_framework import serializers

from railway.models import (
    Station,
    Route,
    TrainType,
    Train,
    Journey,
    Crew
)


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    destination = serializers.CharField(source="destination.name", read_only=True)


class TrainTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "carriages",
            "seats_in_carriage",
            "train_type"
        )


class TrainListSerializer(TrainSerializer):
    train_type = serializers.CharField(
        source="train_type.name",
        read_only=True
    )


class JourneySerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.select_related("source", "destination")
    )

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "train",
            "departure_time",
            "arrival_time"
        )


class JourneyListSerializer(JourneySerializer):
    route = serializers.StringRelatedField(read_only=True)
    train_name = serializers.CharField(
        source="train.name",
        read_only=True
    )

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "train_name",
            "departure_time",
            "arrival_time"
        )


class JourneyRetrieveSerializer(JourneySerializer):
    route = RouteListSerializer(read_only=True)
    train = TrainListSerializer(read_only=True)


class CrewSerializer(serializers.ModelSerializer):
    journeys = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Journey.objects.select_related(
            "route",
            "route__source",
            "route__destination",
            "train",
        )
    )

    class Meta:
        model = Crew
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "journeys"
        )


class CrewListSerializer(CrewSerializer):
    journeys_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Crew
        fields = (
            "id",
            "full_name",
            "journeys_count"
        )


class CrewRetrieveSerializer(CrewSerializer):
    journeys = JourneyListSerializer(many=True, read_only=True)
