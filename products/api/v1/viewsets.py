from rest_framework import viewsets, response, status
from users.permissions import IsAdvisor
from ...models import Product, AdvisorProductLink
from .serializers import ProductSerializer, AdvisorProductLinkSerializer
from ...permissions import IsAdmin


class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdvisor() or IsAdmin()]
        else:
            return [IsAdmin()]


class AdvisorProductLinkViewSet(viewsets.ModelViewSet):
    queryset = AdvisorProductLink.objects.all()
    serializer_class = AdvisorProductLinkSerializer
    http_methods = ['post']
    permission_classes = [IsAdvisor]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)