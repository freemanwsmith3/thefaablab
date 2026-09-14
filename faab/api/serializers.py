"""
Serializers.

Deliberately thin: every expensive value is precomputed on BidAggregate, so
these move numbers rather than deriving them. The old SerializerMethodFields
that reached back into the ORM per row are gone.
"""
from typing import Optional

from rest_framework import serializers

from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    """Legacy player shape. team/position come from select_related, not queries."""

    team = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'name', 'team', 'position', 'link', 'image', 'sleeper_id', 'target_id']

    def get_team(self, obj) -> Optional[str]:
        return obj.team.team_name if obj.team_id else None

    def get_position(self, obj) -> Optional[str]:
        return obj.position.position_type if obj.position_id else None

    def get_target_id(self, obj) -> Optional[int]:
        # Prefetched by the view; never triggers a query here.
        return self.context.get('target_ids', {}).get(obj.id)


class BidInputSerializer(serializers.Serializer):
    """Validates an incoming crowd bid. Week is the legacy running counter."""

    player = serializers.IntegerField(min_value=1)
    week = serializers.IntegerField(min_value=0, max_value=2000)
    value = serializers.IntegerField(min_value=0, max_value=100)


# ---------------------------------------------------------------------------
# Response schemas
#
# These exist to document the API rather than to serialise it -- the views
# build plain dicts from precomputed aggregate columns, which is faster than
# running a serialiser per row. Keeping them in sync with the views is manual,
# so they are deliberately small.
# ---------------------------------------------------------------------------
class BinSerializer(serializers.Serializer):
    label = serializers.CharField(help_text='Display label, e.g. "10 - 20".')
    lo = serializers.IntegerField()
    hi = serializers.IntegerField()
    bids = serializers.IntegerField(help_text='Bids falling in this bin.')


class WinCurvePointSerializer(serializers.Serializer):
    bid = serializers.IntegerField(help_text='Bid as percent of budget.')
    win_pct = serializers.FloatField(
        help_text='Share of observed leagues this bid would have won.'
    )


class CrowdStatsSerializer(serializers.Serializer):
    """What visitors said they would bid."""

    n = serializers.IntegerField(help_text='Number of bids.')
    mean = serializers.FloatField(allow_null=True)
    median = serializers.FloatField(allow_null=True)
    mode = serializers.IntegerField(allow_null=True)
    p25 = serializers.FloatField(allow_null=True)
    p75 = serializers.FloatField(allow_null=True)
    bins = BinSerializer(many=True)


class MarketStatsSerializer(serializers.Serializer):
    """What real Sleeper leagues paid, as percent of budget."""

    n = serializers.IntegerField(help_text='Bids observed, winners and losers.')
    n_leagues = serializers.IntegerField(
        help_text='Leagues where this player was actually claimed.'
    )
    mean = serializers.FloatField(allow_null=True)
    median = serializers.FloatField(allow_null=True)
    mode = serializers.IntegerField(allow_null=True)
    p25 = serializers.FloatField(allow_null=True)
    p75 = serializers.FloatField(allow_null=True)
    bins = BinSerializer(many=True)
    win_curve = WinCurvePointSerializer(
        many=True, help_text='P(win) for every bid 0-100.'
    )
    bid_to_win_80 = serializers.IntegerField(
        allow_null=True, help_text='Smallest bid that would have won 80% of leagues.'
    )


class WeekPlayerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    team = serializers.CharField(allow_null=True)
    position = serializers.CharField(allow_null=True)
    image = serializers.CharField(allow_null=True)
    sleeper_id = serializers.CharField(allow_null=True)
    target_id = serializers.IntegerField(allow_null=True)
    crowd = CrowdStatsSerializer(allow_null=True)
    market = MarketStatsSerializer(allow_null=True)


class WeekFiltersSerializer(serializers.Serializer):
    size = serializers.IntegerField(help_text='League size; 0 means all sizes.')
    scoring = serializers.CharField(help_text='all | ppr | half | std')
    limit = serializers.IntegerField(help_text='Max players returned.')


class WeekResponseSerializer(serializers.Serializer):
    season = serializers.IntegerField(allow_null=True)
    week = serializers.IntegerField(allow_null=True)
    filters = WeekFiltersSerializer()
    players = WeekPlayerSerializer(many=True)


class TargetsResponseSerializer(serializers.Serializer):
    players = PlayerSerializer(many=True)


class LegacyStatSerializer(serializers.Serializer):
    """Original shape. Fields are strings when no bids exist yet."""

    averageBid = serializers.CharField(help_text='Number, or "NA".')
    medianBid = serializers.CharField(help_text='Number, or "NA".')
    mostCommonBid = serializers.CharField(help_text='Number, or "NA".')
    numberOfBids = serializers.CharField(
        help_text='Count, or "You\'re the 1st bid".'
    )


class StatsResponseSerializer(serializers.Serializer):
    binned_data = serializers.DictField(
        child=BinSerializer(many=True), help_text='Keyed by player id.'
    )
    stats = serializers.DictField(
        child=LegacyStatSerializer(), help_text='Keyed by player id.'
    )


class BidResultSerializer(serializers.Serializer):
    recorded = serializers.BooleanField()
    reason = serializers.CharField(
        required=False, help_text='"zero_bid" or "duplicate" when not recorded.'
    )


class HealthSerializer(serializers.Serializer):
    status = serializers.CharField()
