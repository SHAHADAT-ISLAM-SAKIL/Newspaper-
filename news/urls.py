from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CategoryViewSet, RatingViewSet
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Add media URL patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
