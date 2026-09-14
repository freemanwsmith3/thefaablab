from django.contrib import admin

from .models import BidAggregate, MarketBid, Player, SleeperLeague


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'team', 'position', 'sleeper_id')
    search_fields = ('name', 'sleeper_id')
    list_select_related = ('team', 'position')


@admin.register(SleeperLeague)
class SleeperLeagueAdmin(admin.ModelAdmin):
    list_display = ('league_id', 'season', 'total_rosters', 'waiver_budget',
                    'scoring', 'is_active', 'last_ingested_week')
    list_filter = ('season', 'is_active', 'scoring', 'total_rosters')
    search_fields = ('league_id',)


@admin.register(MarketBid)
class MarketBidAdmin(admin.ModelAdmin):
    list_display = ('sleeper_player_id', 'season', 'week', 'bid_raw', 'budget',
                    'bid_pct', 'won')
    list_filter = ('season', 'week', 'won')
    raw_id_fields = ('league', 'player')


@admin.register(BidAggregate)
class BidAggregateAdmin(admin.ModelAdmin):
    list_display = ('scope', 'player', 'season', 'week', 'league_size', 'scoring',
                    'n', 'mean', 'median')
    list_filter = ('scope', 'season', 'week', 'scoring')
    raw_id_fields = ('player',)
