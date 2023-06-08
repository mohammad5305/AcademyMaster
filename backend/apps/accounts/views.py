from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import (
    AccountRegisterSerializer,
    AccountVerifySerializer
)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)


@extend_schema_view(
    post=extend_schema(
        description='''Register a new user.''',
        request=AccountRegisterSerializer,
        responses={
            '200': 'User already exists and pending to verification',
            '201': 'ok',
            '400': 'An active user already exists',
        },
        tags=['Authentication'],
    ),
)
class UserRegisterView(CreateAPIView):
    serializer_class = AccountRegisterSerializer


@extend_schema_view(
    post=extend_schema(
        description='''Verify an account.''',
        request=AccountVerifySerializer,
        responses={
            '200': 'User already exists and pending to verification',
            '409': 'User is already verified',
            '400': 'Invalid token',
        },
        tags=['Authentication'],
    ),
)
class UserVerifyView(APIView):
    serializer_class = AccountVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.verify_code(
                email=serializer.validated_data['email'],
                code=serializer.validated_data['code'],
            )
            return Response("Account verified", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        description='''Return Access/Refresh Token''',
        responses={
            '200': 'Success',
            '400': 'Invalid data',
        },
        tags=['Authentication'],
    ),
)
class TokenObtainView(TokenObtainPairView):
    pass
