from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer
from django.db.models import Count, Avg, ExpressionWrapper, F, DurationField
from django.utils import timezone

class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        vendor = generics.get_object_or_404(Vendor, pk=vendor_id)
        calculate_vendor_performance_metrics(vendor.id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

def update_vendor_performance_metrics(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
    total_completed_pos = completed_pos.count()
    on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100 if total_completed_pos > 0 else 0

    quality_rating_avg = completed_pos.exclude(quality_rating__isnull=True).aggregate(average_rating=Avg('quality_rating'))['average_rating'] or 0

    response_times = completed_pos.exclude(acknowledgment_date__isnull=True).annotate(
        response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
    ).aggregate(avg_response_time=Avg('response_time'))['avg_response_time'] or 0

    fulfilled_pos = completed_pos.exclude(delivery_date__isnull=True)
    fulfilment_rate = (fulfilled_pos.count() / total_completed_pos) * 100 if total_completed_pos > 0 else 0

    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = quality_rating_avg
    vendor.average_response_time = response_times.total_seconds() / 60
    vendor.fulfilment_rate = fulfilment_rate
    vendor.save()

def calculate_vendor_performance_metrics(vendor_id):
    vendor = Vendor.objects.get(pk=vendor_id)
    update_vendor_performance_metrics(vendor)

def update_purchase_order_performance_metrics(po_id):
    po = PurchaseOrder.objects.get(pk=po_id)
    vendor = po.vendor
    update_vendor_performance_metrics(vendor)

def create_historical_performance_record(vendor_id):
    vendor = Vendor.objects.get(pk=vendor_id)
    HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfilment_rate=vendor.fulfilment_rate
    )
