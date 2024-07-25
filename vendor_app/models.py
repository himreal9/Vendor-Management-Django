from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=100, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    orders = PurchaseOrder.objects.filter(vendor=vendor)

    total_orders = orders.count()
    on_time_orders = orders.filter(delivery_date__lte=instance.delivery_date).count()
    vendor.on_time_delivery_rate = on_time_orders / total_orders if total_orders > 0 else 0

    quality_ratings = orders.filter(quality_rating__isnull=False).values_list('quality_rating', flat=True)
    vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0

    response_times = orders.filter(acknowledgment_date__isnull=False).annotate(
        response_time=models.ExpressionWrapper(
            models.F('acknowledgment_date') - models.F('issue_date'),
            output_field=models.DurationField()
        )
    ).values_list('response_time', flat=True)
    average_response_time = sum(response_times, datetime.timedelta()) / len(response_times) if response_times else datetime.timedelta()
    vendor.average_response_time = average_response_time.total_seconds() / 3600  # in hours

    fulfilled_orders = orders.filter(status='completed').count()
    vendor.fulfillment_rate = fulfilled_orders / total_orders if total_orders > 0 else 0

    vendor.save()

    # Save historical performance
    HistoricalPerformance.objects.create(
        vendor=vendor,
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate
    )
