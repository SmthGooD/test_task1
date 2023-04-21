from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from api.views import RestaurantViewSet, MenuViewSet, EmployeeViewSet, vote, results

router = routers.DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('vote/', vote),
    path('results/', results),
    path(r'api/auth/', include('djoser.urls')),
    re_path(r'auth/', include('djoser.urls.authtoken')),
]
