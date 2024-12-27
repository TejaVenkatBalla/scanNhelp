from django.urls import path
from .views import index ,signup #, SigninView
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserViewSet, ProductViewSet

urlpatterns = [
    #ping
    path("a/", index),

    #auth 
    path('signup/', signup, name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # User URLs
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),

    # Product URLs
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='product-detail'),
]
