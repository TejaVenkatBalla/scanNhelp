# views.py
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
# views.py
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView


@api_view(['POST'])
def scan_tag(request):
    tag_id = request.data.get('tag_id')
    tag_type = request.data.get('tag_type')

    if not tag_id or not tag_type:
        return JsonResponse({"error": "tag_id and tag_type are required"}, status=400)

    # Check if the tag is already registered
    product = Product.objects.filter(tag_id=tag_id, tag_type=tag_type).first()

    if product and product.display:  # If tag exists
        if product.tag_type == 1:  # For products, return owner contact details
            product_info = {
                "Product Name": product.product_name,
                "Owner": product.owner.name,
                "Description" : product.description,                
            }
            contact_info = {
                "Name": product.contact_name,
                "Phone Number": product.contact_phone,
                "Alternate Number": product.contact_alternate_number,
                "Address": product.contact_address,
            }
            reward_info = {
                "Reward Amount": product.reward_amount,
                "Note": product.note,
            }
            return JsonResponse({"Product Information": product_info, "Contact Information": contact_info, "Reward Information": reward_info}, status=200)

        if product.tag_type == 2:  # For vehicles, return owner medical details
            product_info = {
                "Product Name": product.product_name,
                "Owner": product.owner.name,
                "Description" : product.description,                
            }
            contact_info = {
                "Name": product.contact_name,
                "Phone Number": product.contact_phone,
                "Alternate Number": product.contact_alternate_number,
                "Address": product.contact_address,
            }
            medical_data = {
                "Emergency Contact":product.Emergency_Contact,
                "Blood Group": product.blood_group,
                "Existing Health Issues": product.existing_health_issues,
                "Existing Medication": product.existing_medication,
                "Primary Doctor": product.primary_doctor,
                "Allergies": product.allergies,
                "Physically Disabled": product.physically_disabled,
            }
            return JsonResponse({"Product Information": product_info, "Contact Information": contact_info,"Medical Details": medical_data}, status=200)

    elif product and not product.display:  # If tag exists but not displayed
        return JsonResponse({"Message": "product display is off"}, status=200)
    
    else:
        return JsonResponse({"error": "Product not found please Login/Register and add the product"}, status=200)
    


@api_view(['GET'])
def index(request):
    return HttpResponse("hi")



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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] 


class ProductView(APIView):
    permission_classes = [IsAuthenticated]          # Ensures only authenticated users can access this view

    
    def get(self, request, pk=None):
        """Return all products of a user or a specific product by ID."""
        user_id = request.query_params.get('user_id')  # Use query parameters for user_id
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        if pk is not None:
            # Get a specific product by ID
            try:
                product = Product.objects.get(pk=pk,owner_id=user_id)
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Return all products of a user
            products = Product.objects.filter(owner_id=user_id)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        """Add a new product."""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Modify an existing product."""
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a product."""
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)