from rest_framework import serializers

from railway.models import (
    Station,
    Route,
    TrainType,
    Train
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
