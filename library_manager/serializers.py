from rest_framework import serializers

class CheckoutSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=True) 
    member_id = serializers.IntegerField(required=True)
    date = serializers.DateField(required=True)
    
class ReturnSerializer(CheckoutSerializer):
    pass

class FulfillSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=True)
    date = serializers.DateField(required=True)
