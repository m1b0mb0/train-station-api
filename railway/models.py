from django.db import models


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
