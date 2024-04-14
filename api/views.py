from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view
from .models import Product, Material, ProductMaterial, PartialWarehouse
from .serializers import (
    ProductInfoSerializer,
    ProductSerializer,
    MaterialSerializer,
    ProductMaterialSerializer,
    PartialWarehouseSerializer
)

# Custom function to request on products

@api_view(['GET'])
def product_info(request):
    # step 1: make sure request has data attached
    if not request.data or not request.data.get('data'):
        return Response({'message': 'your request body should have data attached'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data.get('data')

    # step 2: loop each requested product and check if it is really valid
    for product_req_data in data:
        serializer = ProductInfoSerializer(data=product_req_data)
        # if data is not valid return errors
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # step 3: loop and calculat how much materials we need for each product requested
    used_material_ids = set()  # Using a set to avoid duplicate material_ids
    for product in data:
        # set product name
        product['product_name'] = Product.objects.get(pk=product['product_id']).name

        query = ProductMaterial.objects.filter(product_id=product['product_id'])

        materials_required = []
        
        for q in query:
            materials_required.append({
                'material_name': q.material.name,
                'material_id': q.material_id,
                'total_quantity': q.quantity * product['quantity']
            })
            used_material_ids.add(q.material_id)
        
        # set the result
        product['materials_required'] = materials_required

    #  step 4: get all Partial Warehouses that has materials we need
    warehouses_query = PartialWarehouse.objects.filter(material_id__in=list(used_material_ids))
    warehouses = []
    for wh in warehouses_query:
        warehouses.append({
            'id': wh.id,
            'material_id': wh.material_id,
            'remainder': wh.remainder,
            'price': wh.price
        })

    # step 5: finally compare and get results
    result = []
    for product in data:
        product_materials = []
        for material in product['materials_required']:
            for wh in warehouses:
                # check if materials matches and warehouse has material
                if not wh['material_id'] == material['material_id'] or not wh['remainder'] > 0:
                    continue

                # Calculate how much we should take or we can take from this warehouse
                take_quantity = min(material['total_quantity'], wh['remainder'])
                # Reduce the remainder in the warehouse
                wh['remainder'] -= take_quantity
                material['total_quantity'] -= take_quantity

                product_materials.append({
                    "warehouse_id": wh['id'],
                    "material_name": material['material_name'],
                    "qty": take_quantity,
                    "price": wh['price']
                })

                #  we are done if we took all we need
                if  material['total_quantity'] == 0:
                    break 

            # if there is no more to take from
            if not material['total_quantity'] == 0:
                product_materials.append({
                    "warehouse_id": None,
                    "material_name": material['material_name'],
                    "qty": material['total_quantity'],
                    "price": None
                })


        result.append({
            'product_name': product['product_name'],
            'product_qty': product['quantity'],
            'product_materials': product_materials
        })


    return Response({'result': result}, status=status.HTTP_200_OK)



# Each model has its ViewSet to Retrieve/Create/Update/Delete

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class ProductMaterialViewSet(ModelViewSet):
    queryset = ProductMaterial.objects.all()
    serializer_class = ProductMaterialSerializer


class PartialWarehouseViewSet(ModelViewSet):
    queryset = PartialWarehouse.objects.all()
    serializer_class = PartialWarehouseSerializer