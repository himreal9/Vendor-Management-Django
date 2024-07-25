from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Vendor, PurchaseOrder
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class VendorTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.headers={"HTTP_AUTHORIZATION":'Token ' + self.token.key}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'contact@example.com',
            'address': '123 Test Street',
            'vendor_code': 'V001'
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def test_create_vendor(self):
        url = reverse('vendor-list')
        data = {
            'name': 'New Vendor',
            'contact_details': 'newcontact@example.com',
            'address': '456 New Avenue',
            'vendor_code': 'V002'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_vendors(self):
        url = reverse('vendor-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_vendor(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor_data['name'])

    def test_update_vendor(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.id})
        data = {
            'name': 'Updated Vendor',
            'contact_details': 'updatedcontact@example.com',
            'address': '789 Updated Street',
            'vendor_code': 'V003'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, data['name'])

    def test_delete_vendor(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

class PurchaseOrderTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.headers={"HTTP_AUTHORIZATION":'Token ' + self.token.key}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='contact@example.com',
            address='123 Test Street',
            vendor_code='V001'
        )
        self.purchase_order_data = {
            'po_number': 'PO001',
            'vendor': self.vendor,
            'order_date': timezone.now(),
            'delivery_date': timezone.now() + datetime.timedelta(days=7),
            'items': [{'item': 'item1', 'quantity': 10}],
            'quantity': 10,
            'status': 'completed',
            'quality_rating': 4.5,
            'issue_date': timezone.now(),
            'acknowledgment_date': timezone.now() + datetime.timedelta(days=1)
        }
        self.purchase_order = PurchaseOrder.objects.create(**self.purchase_order_data)

    def test_create_purchase_order(self):
        url = reverse('purchaseorder-list')
        data = {
            'po_number': 'PO002',
            'vendor': self.vendor.id,
            'order_date': timezone.now(),
            'delivery_date': timezone.now() + datetime.timedelta(days=10),
            'items': [{'item': 'item2', 'quantity': 5}],
            'quantity': 5,
            'status': 'pending',
            'issue_date': timezone.now()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_purchase_orders(self):
        url = reverse('purchaseorder-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_purchase_order(self):
        url = reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], self.purchase_order_data['po_number'])

    def test_update_purchase_order(self):
        url = reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.id})
        data = {
            'po_number': 'PO003',
            'vendor': self.vendor.id,
            'order_date': timezone.now(),
            'delivery_date': timezone.now() + datetime.timedelta(days=15),
            'items': [{'item': 'item3', 'quantity': 20}],
            'quantity': 20,
            'status': 'completed',
            'issue_date': timezone.now()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.po_number, data['po_number'])

    def test_delete_purchase_order(self):
        url = reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)
    
    def test_vendor_performance_metrics(self):
        url = reverse('vendor-performance', kwargs={'pk': self.vendor.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('on_time_delivery_rate', response.data)
        self.assertIn('quality_rating_avg', response.data)
        self.assertIn('average_response_time', response.data)
        self.assertIn('fulfillment_rate', response.data)
