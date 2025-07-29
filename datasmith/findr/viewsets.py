from django.contrib.gis.geos import Point
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    @action(detail=False, methods=["get"], url_path="search")
    def search_by_point(self, request):
        from django.core.cache import cache
        try:
            lat = float(request.query_params.get("lat"))
            lng = float(request.query_params.get("lng"))
        except (TypeError, ValueError):
            return Response(
                {"error": "lat and lng query params required and must be float."}, status=status.HTTP_400_BAD_REQUEST
            )
        cache_key = f"servicearea_search_{lat}_{lng}"
        data = cache.get(cache_key)
        if data is None:
            point = Point(lng, lat)
            areas = ServiceArea.objects.filter(geojson__contains=point)
            data = [
                {
                    "polygon_name": area.name,
                    "provider_name": area.provider.name,
                    "price": area.price,
                }
                for area in areas
            ]
            cache.set(cache_key, data, timeout=60 * 5)  # Cache for 5 minutes
        return Response(data, status=status.HTTP_200_OK)
