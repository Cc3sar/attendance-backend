from django.urls import include, path
from knox import views as knox_views
from rest_framework import routers

from api.viewsets import AuthViewSet, ScheduleViewset, UserViewset


router = routers.DefaultRouter()

router.register(r'users', UserViewset)
router.register(r'schedule', ScheduleViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', AuthViewSet.as_view(), name='knox_login'),
    path('auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
]