from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder

class VendorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_vendor_creation(self):
        response = self.client.post('/api/vendors/', {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Test St, Test City',
            'vendor_code': 'V001'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_purchase_order_creation(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='123 Test St, Test City', vendor_code='V001')

        response = self.client.post('/api/purchase_orders/', {
            'po_number': 'PO001',
            'vendor': vendor.id,
            'order_date': '2024-05-10T10:00:00Z',
            'items': [{'name': 'Item1', 'quantity': 10}],
            'quantity': 10,
            'status': 'completed',
            'delivery_date': '2024-05-15T10:00:00Z',
            'quality_rating': 4
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
