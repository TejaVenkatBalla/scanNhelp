# views.py
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from .models import Product, User
from .serializers import ProductSerializer

#from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def check_or_register_tag(request):
    tag_id = request.data.get('tag_id')
    tag_type = request.data.get('tag_type')

    if not tag_id or not tag_type:
        return JsonResponse({"error": "tag_id and tag_type are required"}, status=400)

    # Check if the tag is already registered
    product = Product.objects.filter(tag_id=tag_id, tag_type=tag_type).first()

    if product:  # If tag exists, return product and user details
        user_data = {
            "name": product.owner.name,
            "email": product.owner.email,
            "phone": product.owner.phone,
            "address": product.owner.address
        }
        return JsonResponse({
            "product_details": ProductSerializer(product).data,
            "owner_details": user_data
        }, status=200)

    else:  # If tag does not exist, register the product/vehicle
        user = request.user  # Assuming you want to associate the tag with the logged-in user
        
        if not user:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        # Get product/vehicle details from the request body
        name = request.data.get('name')
        description = request.data.get('description')

        if not name or not description:
            return JsonResponse({"error": "Name and description are required"}, status=400)

        # Register the product/vehicle to the logged-in user
        try:
            product = Product.objects.create(
                name=name,
                description=description,
                tag_id=tag_id,
                tag_type=tag_type,
                owner=user
            )
            return JsonResponse(ProductSerializer(product).data, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@api_view(['GET'])
def index(request):
    return HttpResponse("hi")

# views.py
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User

@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    name = request.data.get('name')
    password = request.data.get('password')
    phone = request.data.get('phone')
    address = request.data.get('address')

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(
            email=email,
            name=name,
            password=password,
            phone=phone,
            address=address
        )
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User, Product
from .serializers import UserSerializer, ProductSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [IsAuthenticated]  # Only authenticated users can manage products
    def get_queryset(self):
        user_id = self.request.data['user_id']
        if user_id:
            return Product.objects.filter(owner_id=user_id)
        return Product.objects.none() 