from django.urls import path
from .views import index ,signup #, SigninView
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserViewSet, ProductView,scan_tag

urlpatterns = [
    #ping
    path("a/", index),

    #scan api
    path("scan", scan_tag),
    
    #auth 
    path('signup/', signup, name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # User URLs
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),

    # Product URLs
    path('products/user/', ProductView.as_view(), name='get-user-products'),  # For getting all products of a user
    path('products/<int:pk>/', ProductView.as_view(), name='get-product'),  # For getting a specific product by ID
    path('products/add/', ProductView.as_view(), name='add-product'),  # For adding a new product
    path('products/modify/<int:pk>/', ProductView.as_view(), name='modify-product'),  # For modifying a product
    path('products/delete/<int:pk>/', ProductView.as_view(), name='delete-product'),  # For deleting a product
]
