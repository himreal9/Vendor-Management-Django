from django.core.management.base import BaseCommand
from vendor_app.models import Vendor, PurchaseOrder, HistoricalPerformance
from django.utils import timezone
import json
import datetime

class Command(BaseCommand):
    help = 'Create test data for Vendor, Purchase Order, and Historical Performance'

    def handle(self, *args, **kwargs):
        Vendor.objects.all().delete()
        PurchaseOrder.objects.all().delete()
        HistoricalPerformance.objects.all().delete()
        # Create test vendors

        vendor1 = Vendor.objects.create(
            name="Test Vendor 1",
            contact_details="contact1@example.com",
            address="123 Test Street",
            vendor_code="V001"
        )
        vendor2 = Vendor.objects.create(
            name="Test Vendor 2",
            contact_details="contact2@example.com",
            address="456 Test Avenue",
            vendor_code="V002"
        )

        # Create test purchase orders for vendor1
        po1 = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=vendor1,
            order_date=timezone.now(),
            delivery_date=timezone.now() + datetime.timedelta(days=7),
            items=json.dumps([{"item": "item1", "quantity": 10}]),
            quantity=10,
            status="completed",
            quality_rating=4.5,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now() + datetime.timedelta(days=1)
        )

        po2 = PurchaseOrder.objects.create(
            po_number="PO002",
            vendor=vendor1,
            order_date=timezone.now(),
            delivery_date=timezone.now() + datetime.timedelta(days=10),
            items=json.dumps([{"item": "item2", "quantity": 5}]),
            quantity=5,
            status="pending",
            issue_date=timezone.now()
        )

        # Create test purchase orders for vendor2
        po3 = PurchaseOrder.objects.create(
            po_number="PO003",
            vendor=vendor2,
            order_date=timezone.now(),
            delivery_date=timezone.now() + datetime.timedelta(days=5),
            items=json.dumps([{"item": "item3", "quantity": 20}]),
            quantity=20,
            status="completed",
            quality_rating=5.0,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now() + datetime.timedelta(hours=5)
        )

        po4 = PurchaseOrder.objects.create(
            po_number="PO004",
            vendor=vendor2,
            order_date=timezone.now(),
            delivery_date=timezone.now() + datetime.timedelta(days=3),
            items=json.dumps([{"item": "item4", "quantity": 15}]),
            quantity=15,
            status="pending",
            issue_date=timezone.now()
        )

        # Create historical performance records
        for vendor in [vendor1, vendor2]:
            HistoricalPerformance.objects.create(
                vendor=vendor,
                date=timezone.now(),
                on_time_delivery_rate=vendor.on_time_delivery_rate,
                quality_rating_avg=vendor.quality_rating_avg,
                average_response_time=vendor.average_response_time,
                fulfillment_rate=vendor.fulfillment_rate
            )

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
