from django.test import TestCase

from .models import Vendor, Purchase_Order
from .serializers import VendorSerializer, Purchase_OrderSerializer
# Create your tests here.

class vendorTestCase(TestCase):
    def setUp(self):
        self.vendor_data = {
            'name': 'Vendor 1',
            'contact_details': 'Contact details 1',
            'address': 'Address 1',
            'vendor_code': 'VENDOR001'
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def test_create_vendor(self):
        obj_data = Vendor.objects.get(name="Vendor 1")
        self.assertEqual(obj_data.name, 'Vendor 1')


    def test_retrieve_vendor(self):
        self.assertEqual(self.vendor_data, VendorSerializer(self.vendor).data)

   
class Purchase_OrderTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name='Vendor 1', contact_details='Contact details 1', address='Address 1', vendor_code='VENDOR001')
        self.purchase_order_data = {
            'po_number': 'PO001',
            'vendor': self.vendor.id,
            'order_date': '2024-05-01T00:00:00Z',
            'delivery_date': '2024-05-05T00:00:00Z',
            'items': {'name': 'Item 1'},
            'quantity': 5,
            'status': 'pending'
        }
        self.purchase_order = Purchase_Order.objects.create(**self.purchase_order_data)

    def test_create_purchase_order(self):
        self.assertEqual(self.purchase_order_data, Purchase_OrderSerializer(self.purchase_order).data)