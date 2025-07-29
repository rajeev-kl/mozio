from django.test import TestCase
from django.contrib.gis.geos import Polygon
from rest_framework.test import APIClient
from .models import Provider, ServiceArea

class ProviderModelTest(TestCase):
    def test_create_provider(self):
        provider = Provider.objects.create(
            name="Test Provider",
            email="test@example.com",
            phone_number="+1234567890",
            language="en",
            currency="USD",
        )
        self.assertEqual(provider.name, "Test Provider")
        self.assertEqual(provider.email, "test@example.com")

class ServiceAreaModelTest(TestCase):
    def setUp(self):
        self.provider = Provider.objects.create(
            name="Test Provider",
            email="test@example.com",
            phone_number="+1234567890",
            language="en",
            currency="USD",
        )

    def test_create_service_area(self):
        poly = Polygon(((0,0), (0,1), (1,1), (1,0), (0,0)))
        area = ServiceArea.objects.create(
            provider=self.provider,
            name="Test Area",
            price=50.0,
            geojson=poly,
        )
        self.assertEqual(area.name, "Test Area")
        self.assertEqual(area.provider, self.provider)

class ServiceAreaAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.provider = Provider.objects.create(
            name="Test Provider",
            email="test@example.com",
            phone_number="+1234567890",
            language="en",
            currency="USD",
        )
        self.poly = Polygon(((0,0), (0,1), (1,1), (1,0), (0,0)))
        self.area = ServiceArea.objects.create(
            provider=self.provider,
            name="Test Area",
            price=50.0,
            geojson=self.poly,
        )

    def test_list_service_areas(self):
        response = self.client.get("/api/service-areas/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

    def test_search_by_point(self):
        response = self.client.get("/api/service-areas/search", {"lat": 0.5, "lng": 0.5})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(area["polygon_name"] == "Test Area" for area in response.data))

    def test_create_provider_api(self):
        data = {
            "name": "API Provider",
            "email": "api@example.com",
            "phone_number": "+1234567891",
            "language": "en",
            "currency": "USD"
        }
        response = self.client.post("/api/providers/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "API Provider")
