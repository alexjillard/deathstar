from datetime import datetime, timezone
import requests
from django.db import models


class ChargeManager(models.Manager):
    def active(self):
        try:
            return self.filter(depleted=False).order_by('-started_at')[0]
        except IndexError:
            return self.create()

class Charge(models.Model):

    objects = ChargeManager()

    percent = models.PositiveSmallIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    depleted_at = models.DateTimeField(null=True)
    depleted = models.BooleanField(default=False)

    @property
    def charged(self) -> bool:
        return self.percent >= 100

    def increment(self):
        if self.percent < 100:
            now = datetime.now().replace(tzinfo=timezone.utc)
            self.percent = min((now - self.started_at).total_seconds() * 3, 100)
            self.save()

    def use_charge(self):
        self.depleted_at = datetime.now()
        self.depleted = True
        self.save()


class PlanetManager(models.Manager):
    def active(self):
        try:
            return self.filter(destroyed=False).order_by('-created_at')[0]
        except IndexError:
            return self.find_planet()

    def find_planet(self):
        data = requests.get('https://randomuser.me/api/').json()
        planet_name = data.get('results')[0].get('location').get('city')

        print(planet_name)

        planet = self.create(
            name=planet_name
        )
        return planet



class Planet(models.Model):
    objects = PlanetManager()

    name = models.CharField(max_length=255)
    destroyed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    destroyed_at = models.DateTimeField(null=True)

    def destroy(self):
        self.destroyed = True
        self.destroyed_at = datetime.now()
        self.save()