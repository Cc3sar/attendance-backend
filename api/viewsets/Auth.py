from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import AllowAny

from api.serializers import AuthLoginSerializer


class AuthViewSet(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(AuthViewSet, self).post(request, format=None)