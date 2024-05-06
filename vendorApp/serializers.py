from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        # fields = ['id','name']
        validators = [
            UniqueTogetherValidator(
                queryset=Vendor.objects.all(),
                fields=['vendor_code']
            )
        ]
        extra_kwargs = {
            'vendor_code': {
                'validators': [
                    UniqueValidator(
                        queryset=Vendor.objects.all()
                    )
                ],
                'max_length': 100
            }
        }


class Vendor_PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name','on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


class Purchase_OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase_Order
        # fields = ['po_number','vendor','items','quantity']
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Purchase_Order.objects.all(),
                fields=['po_number']
            )
        ]
        extra_kwargs = {
            'po_number': {
                'validators': [
                    UniqueValidator(
                        queryset=Purchase_Order.objects.all()
                    )
                ],
                'max_length': 100
            },
            'quantity': {
                'min_value': 0,
            },
            'quality_rating': {
                'min_value': 0,
                'max_value': 5,
            },
        }


class Purchase_Order_AckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase_Order
        fields = ['status']


class Historical_PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historical_Performance
        fields = '__all__'
