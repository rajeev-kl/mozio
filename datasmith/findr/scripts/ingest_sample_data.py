import math
import random

from django.contrib.gis.geos import Polygon
from findr.models import Provider, ServiceArea

LANGUAGES = ["en", "es", "fr", "de", "it"]
CURRENCIES = ["USD", "EUR", "GBP", "INR", "JPY"]


def random_polygon(center_x, center_y, size=0.1):
    # Create a random polygon with 3-20 points in a rough circle
    num_points = random.randint(3, 20)
    angle_step = 360 / num_points
    points = []
    for i in range(num_points):
        angle = (angle_step * i) * (3.14159 / 180)
        # Add some jitter to the radius for irregularity
        radius = size * random.uniform(0.8, 1.2)
        x = center_x + radius * random.uniform(0.95, 1.05) * math.cos(angle)
        y = center_y + radius * random.uniform(0.95, 1.05) * math.sin(angle)
        points.append((x, y))
    # Ensure the polygon is closed
    points.append(points[0])
    return Polygon(points)


def run():
    Provider.objects.all().delete()
    ServiceArea.objects.all().delete()
    # Generate base centers for each provider to encourage overlap
    provider_centers = [
        (random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(100)
    ]

    for i in range(100):
        provider = Provider.objects.create(
            name=f"Provider {i+1}",
            email=f"provider{i+1}@example.com",
            phone_number=f"+123456789{i+1}",
            language=random.choice(LANGUAGES),
            currency=random.choice(CURRENCIES),
        )
        num_areas = random.randint(1, 10)
        # Pick a base center for this provider
        base_x, base_y = provider_centers[i]
        for j in range(num_areas):
            # Overlap with other providers by picking a center from another provider
            overlap_with = random.choice([
                idx for idx in range(100) if idx != i
            ])
            overlap_x, overlap_y = provider_centers[overlap_with]
            # Blend the centers for overlap
            center_x = (base_x + overlap_x) / 2 + random.uniform(-0.02, 0.02)
            center_y = (base_y + overlap_y) / 2 + random.uniform(-0.02, 0.02)
            poly = random_polygon(center_x, center_y, size=0.1 + 0.01 * j)
            ServiceArea.objects.create(
                provider=provider,
                name=f"Area {j+1} of Provider {i+1}",
                price=round(random.uniform(10, 100), 2),
                geojson=poly,
            )
    print("Sample data created.")
