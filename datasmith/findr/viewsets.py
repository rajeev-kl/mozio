
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
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
        try:
            lat = float(request.query_params.get("lat"))
            lng = float(request.query_params.get("lng"))
        except (TypeError, ValueError):
            return Response({"error": "lat and lng query params required and must be float."}, status=status.HTTP_400_BAD_REQUEST)
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
        return Response(data, status=status.HTTP_200_OK)
