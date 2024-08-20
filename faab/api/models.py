from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg, Count
# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=50, unique = True)
    abbreviation = models.CharField(max_length=4, unique = True)

class Position(models.Model):
    position_type = models.CharField(max_length=50, unique = True)

class Player(models.Model):
    name = models.CharField(max_length=50, unique = True)
    team = models.ForeignKey(Team,  on_delete=models.CASCADE, related_name="teams", null=True)
    position = models.ForeignKey(Position,  on_delete=models.CASCADE, related_name="positions", null=True)
    link = models.CharField(max_length=256, unique = True, null=True)
    image = models.CharField(max_length=256, unique = True, null=True)
    
    @property
    def average_rank(self):
        return Ranking.objects.all().aggregate(avg_rank=models.Avg('rank'))['avg_rank'] 


class Target(models.Model):
    player = models.ForeignKey(Player,  on_delete=models.CASCADE, related_name="targets")
    week = models.IntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(2000)])

    @property
    def num_valid_bids(self):
        return Bid.objects.filter(target = self.id, value__range = [1, 100]).count()

    @property
    def mean_value(self):
        return Bid.objects.filter(target = self.id, value__range = [1, 100]).aggregate(Avg('value'))['value__avg']


    @property
    def median_value(self):
        queryset = Bid.objects.filter(target = self.id, value__range = [1, 100])
        count =  queryset.count()
        return queryset.values_list('value', flat=True).order_by('value')[int(round(count/2))]

    @property
    def mode_value(self):
        return Bid.objects.filter(target = self.id, value__range = [1, 100]).values("value").annotate(count=Count('value')).order_by("-count")[0]['value']


class BidOriginal(models.Model):
    value = models.IntegerField(null=False, default=0,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)
    week = models.IntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(2000)])
    user = models.CharField(max_length=50)

class Bid(models.Model):
    value = models.IntegerField(null=False, default=0,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)
    week = models.IntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(2000)])
    user = models.CharField(max_length=50)

class Ranking(models.Model):
    rank = models.IntegerField(null=False, default=0,  validators=[MinValueValidator(0), MaxValueValidator(200)])
    Player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="rankings")
    created_at = models.DateTimeField(auto_now_add=True)
    week = models.IntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(2000)])
    user = models.CharField(max_length=50)
    opponent = models.ForeignKey(Team,  on_delete=models.CASCADE, related_name="opponents", null=True)

class Auction(models.Model):
    rank = models.IntegerField(null=False, default=0,  validators=[MinValueValidator(0), MaxValueValidator(200)])
    Player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="auction_rankings")
