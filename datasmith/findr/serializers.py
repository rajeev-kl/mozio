
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ["id", "name", "email", "phone_number", "language", "currency"]


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    provider = ProviderSerializer(read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all(), source="provider", write_only=True)

    class Meta:
        model = ServiceArea
        geo_field = "geojson"
        fields = ["id", "name", "price", "geojson", "provider", "provider_id"]
