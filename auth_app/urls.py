from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'service-centers', ServiceCenterViewSet, basename='service-centers')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='register_user'),
    path('service-center/create/', AddNewServiceCenterView.as_view(), name="create_service_center"),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('vehicles/all/', GetAllVehiclesAPIView.as_view(), name='vehicle-list'),
    path('vehicle/create/', AddNewVehicleView.as_view(), name="add new vehicle"),
    path('vehicle/<uuid:pk>/', RetrieveUpdateDestroyVehicleView.as_view(), name='vehicle-detail'),
    #service urls
    path('services/all/', GetAllServicesAPIView.as_view(), name='all services'),
    path('services/create/', AddNewServiceView.as_view(), name='create new service'),
    path('services/<uuid:pk>/', RetrieveUpdateDestroyServicesView.as_view(), name='fetrch service update it and delete'),

    path('', include(router.urls)),
]
"""
    GET /service-centers/ – Anyone can view the list of service centers.

    GET /service-centers/<center_id>/ – Anyone can view details of a center.

    POST /service-centers/ – Only service_manager users can create. You already validate this in your AddNewServiceCenter serializer.

    PUT / PATCH / DELETE /service-centers/<center_id>/ – Only the manager assigned to that service center can edit/delete.

"""