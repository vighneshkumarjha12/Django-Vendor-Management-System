from django.urls import path
from . import views

urlpatterns = [
    path('', views.VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('<int:pk>/', views.VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-retrieve-update-destroy'),
    path('performance/', views.VendorPerformanceAPIView.as_view(), name='vendor-performance'),
]
