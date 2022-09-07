from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=50, unique = True)

class Position(models.Model):
    position_type = models.CharField(max_length=50, unique = True)

class Player(models.Model):
    name = models.CharField(max_length=50, unique = True)
    team = models.ForeignKey(Team,  on_delete=models.CASCADE, related_name="teams")
    position = models.ForeignKey(Position,  on_delete=models.CASCADE, related_name="positions")

class Target(models.Model):
    player = models.ForeignKey(Player,  on_delete=models.CASCADE, related_name="targets")
    week = models.IntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(17)])

class Bid(models.Model):
    value = models.IntegerField(null=False, default=0,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)
    week = models.IntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(17)])
    user = models.CharField(max_length=50)

