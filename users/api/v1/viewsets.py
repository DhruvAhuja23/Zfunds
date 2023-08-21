from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from home.utils import RolesEnum
from .serializers import UserSerializer, ClientSerializer, SignupSerializer
from users.models import User
from rest_framework.authtoken.models import Token
from users.permissions import IsAdvisor
from ...models import Client


class AdvisorViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    http_method = ['post', 'get']

    @action(detail=False, methods=['post'])
    def signup(self, request):
        mobile = request.data.get('mobile')

        # Check if a user with the provided mobile number already exists
        # we could have used other route for login separately and if the user tries to signup with same mobile number
        # we can return the error as well both can be implemented
        existing_user = User.objects.filter(mobile=mobile).first()

        if existing_user:
            serializer = self.get_serializer(existing_user)
            token, _ = Token.objects.get_or_create(user=existing_user)

            return Response({
                'message': 'Advisor already exists.',
                'user': serializer.data,
                'token': token.key,
            }, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=RolesEnum.ADVISOR.value)
            user = serializer.instance
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                'message': 'Advisor account created successfully.',
                'user': serializer.data,
                'token': token.key,
            }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[IsAdvisor])
    def add_client(self, request):
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        advisor = self.request.user  # The logged-in advisor
        client_data = serializer.validated_data
        client_serializer = UserSerializer(data={
            'name': client_data['name'],
            'mobile': client_data['mobile'],
            'role': RolesEnum.USER.value
        })
        client_serializer.is_valid(raise_exception=True)
        client_user = client_serializer.save()
        # Create the Client model instance
        client = Client.objects.create(advisor=advisor, client=client_user)
        return Response({
            'message': 'Client added successfully.',
            'client': {
                'id': client.client.id,
                'name': client.client.name,
                'mobile': client.client.mobile,
                'role': client.client.role
            }
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsAdvisor])
    def clients(self, request):
        advisor = request.user
        clients = advisor.clients.all()
        client_users = User.objects.filter(advisors__in=clients)
        client_serializer = UserSerializer(client_users, many=True)
        return Response(client_serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    http_method = ['post', 'get']

    @action(detail=False, methods=['post'])
    def signup(self, request):
        mobile = request.data.get('mobile')

        # Check if a user with the provided mobile number already exists
        existing_user = User.objects.filter(mobile=mobile).first()

        if existing_user:
            serializer = self.get_serializer(existing_user)
            token, _ = Token.objects.get_or_create(user=existing_user)

            return Response({
                'message': 'User already exists.',
                'user': serializer.data,
                'token': token.key,
            }, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=RolesEnum.USER.value)
            user = serializer.instance
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                'message': 'User account created successfully.',
                'user': serializer.data,
                'token': token.key,
            }, status=status.HTTP_201_CREATED)
