from django.db import models
from django.conf import settings


class Station(models.Model):
    name = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="routes_from"
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="routes_to"
    )
    distance = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "destination"],
                name="unique_route"
            ),
            models.CheckConstraint(
                condition=~models.Q(source=models.F("destination")),
                name="source_not_destination"
            )
        ]

    def __str__(self):
        return f"{self.source.name} - {self.destination.name} ({self.distance} km)"


class TrainType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=255)
    carriages_count = models.PositiveIntegerField()
    seats_in_carriage = models.PositiveIntegerField()
    train_type = models.ForeignKey(
        TrainType,
        on_delete=models.CASCADE,
        related_name="trains"
    )

    def __str__(self):
        return (
            f"{self.name} "
            f"({self.carriages_count} carriages, "
            f"{self.seats_in_carriage} seats per carriage)"
        )


class Journey(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="journeys"
    )
    train = models.ForeignKey(
        Train,
        on_delete=models.CASCADE,
        related_name="journeys"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(arrival_time__gt=models.F("departure_time")),
                name="arrival_after_departure"
            )
        ]

    def __str__(self):
        return f"{self.route} | {self.train.name} | {self.departure_time}"


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    journeys = models.ManyToManyField(Journey, related_name="crews")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    def __str__(self):
        return str(self.created_at)
