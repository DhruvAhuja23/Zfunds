from rest_framework import serializers
from ...models import Product, ProductCategory, AdvisorProductLink
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(max_length=50)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = instance.category.name
        return representation

    def create(self, validated_data):
        category_name = validated_data.pop('category')
        category, _ = ProductCategory.objects.get_or_create(name=category_name)
        validated_data['category'] = category
        product = Product.objects.create(**validated_data)
        return product


class AdvisorProductLinkSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='user'))
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    link = serializers.CharField(read_only=True)  # Read-only field for the generated link

    class Meta:
        model = AdvisorProductLink
        fields = ['user_id', 'product_id', 'link']

    def create(self, validated_data):
        advisor = self.context['request'].user
        user_id = validated_data['user_id'].id
        product_id = validated_data['product_id'].id

        advisor_product_link, created = AdvisorProductLink.objects.get_or_create(
            advisor=advisor,
            user_id=user_id,
            product_id=product_id,
        )
        if created:
            link = f"unique_link_{user_id}_{product_id}"  # link based on your requirements
            advisor_product_link.link = link
            advisor_product_link.save()
        return advisor_product_link
