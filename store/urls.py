from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('products/<int:product_pk>/reviews/', views.ReviewList.as_view()),
    path('products/<int:product_pk>/reviews/<int:pk>/', views.ReviewDetail.as_view()),
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>/', views.CollectionDetail.as_view()),
    path('carts/', views.CartList.as_view()),
    path('carts/<str:pk>/', views.CartDetail.as_view()),
    path('carts/<str:cart_pk>/items/', views.CartItemList.as_view()),
    path('carts/<str:cart_pk>/items/<int:pk>/', views.CartItemDetail.as_view()),
]
