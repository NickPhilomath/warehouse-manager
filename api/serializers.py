from rest_framework import serializers
from .models import Product, Material, ProductMaterial, PartialWarehouse

# product-info request serializer

class ProductInfoSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate(self, data):
        # Check that both product_id and quantity are set.
        if 'product_id' not in data:
            raise serializers.ValidationError("product_id is required")
        if 'quantity' not in data:
            raise serializers.ValidationError("quantity is required")
        return data


# all model serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ProductMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterial
        fields = '__all__'


class PartialWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartialWarehouse
        fields = '__all__'