from rest_framework.routers import DefaultRouter

from .viewsets import ProviderViewSet, ServiceAreaViewSet

router = DefaultRouter()
router.register(r"providers", ProviderViewSet)
router.register(r"service-areas", ServiceAreaViewSet)

urlpatterns = router.urls
