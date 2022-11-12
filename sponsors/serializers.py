
from rest_framework import serializers

from sponsors.models import GenericAsset
from sponsors.models.enums import PublisherChoices, LogoPlacementChoices

class LogoPlacementSerializer(serializers.Serializer):
    publisher = serializers.CharField()
    flight = serializers.CharField()
    sponsor = serializers.CharField()
    sponsor_slug = serializers.CharField()
    description = serializers.CharField()
    logo = serializers.URLField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    sponsor_url = serializers.URLField()
    level_name = serializers.CharField()
    level_order = serializers.IntegerField()


class AssetSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    sponsor = serializers.SerializerMethodField()
    sponsor_slug = serializers.SerializerMethodField()

    class Meta:
        model = GenericAsset
        fields = ["internal_name", "uuid", "value", "content_type", "sponsor", "sponsor_slug"]

    def _get_sponsor_object(self, asset):
        if asset.from_sponsorship:
            return asset.content_object.sponsor
        else:
            return asset.content_object

    def get_content_type(self, asset):
        return asset.content_type.name.title()

    def get_value(self, asset):
        if not asset.has_value:
            return ""
        return asset.value.url if asset.is_file else asset.value

    def get_sponsor(self, asset):
        return self._get_sponsor_object(asset).name

    def get_sponsor_slug(self, asset):
        return self._get_sponsor_object(asset).slug


class FilterLogoPlacementsSerializer(serializers.Serializer):
    publisher = serializers.ChoiceField(
        choices=[(c.value, c.name.replace("_", " ").title()) for c in PublisherChoices],
        required=False,
    )
    flight = serializers.ChoiceField(
        choices=[(c.value, c.name.replace("_", " ").title()) for c in LogoPlacementChoices],
        required=False,
    )

    @property
    def by_publisher(self):
        return self.validated_data.get("publisher")

    @property
    def by_flight(self):
        return self.validated_data.get("flight")

    def skip_logo(self, logo):
        if self.by_publisher and self.by_publisher != logo.publisher:
            return True
        return bool(self.by_flight and self.by_flight != logo.logo_place)


class FilterAssetsSerializer(serializers.Serializer):
    internal_name = serializers.CharField(max_length=128)
    list_empty = serializers.BooleanField(required=False, default=False)

    @property
    def by_internal_name(self):
        return self.validated_data["internal_name"]

    @property
    def accept_empty(self):
        return self.validated_data.get("list_empty", False)
