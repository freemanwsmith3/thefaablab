from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=50, unique = True)
    team = models.CharField(max_length=50)
    mean_value = models.FloatField(null=False, default=0,  validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    week = models.IntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(17)])
    guestCanSee = models.BooleanField(default = False)

class Bid(models.Model):
    value = models.IntegerField(null=False, default=0,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    player = models.ForeignKey(Player,  on_delete=models.CASCADE, related_name="players")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=50, unique = True)