from rest_framework.views import APIView
from library_manager.constants import CHECKOUT_SUCCESSFUL, FULFILMENT_SUCCESSFUL, RESERVATION_SUCCESSFULL, RETURN_SUCCESSFUL
from library_manager.models import Circulation, Reservation
from library_manager.serializers import CheckoutSerializer, ReturnSerializer, FulfillSerializer
from rest_framework.response import Response
from rest_framework import status

class CheckoutBookView(APIView):
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            circulation_id, fail_reason, is_reservation_made = Circulation.checkout_book(validated_data.get("book_id"), validated_data.get("member_id"), validated_data.get("date"))
            
            if fail_reason:
                return Response(fail_reason, status=status.HTTP_400_BAD_REQUEST)
            
            success_reason = RESERVATION_SUCCESSFULL if is_reservation_made else CHECKOUT_SUCCESSFUL
            return Response(success_reason.format(circulation_id), status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReturnBookView(APIView):
    def post(self, request):
        serializer = ReturnSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            circulation_id, fail_reason = Circulation.return_book(validated_data.get("book_id"), validated_data.get("member_id"), validated_data.get("date"))
           
            if fail_reason:
                return Response(fail_reason, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(RETURN_SUCCESSFUL.format(circulation_id), status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FulfillBookView(APIView):
    def post(self, request):
        serializer = FulfillSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            reservation_id, fail_reason = Reservation.fulfil_book(validated_data.get("book_id"), validated_data.get("date"))
            
            if fail_reason:
                return Response(fail_reason, status=status.HTTP_400_BAD_REQUEST)
            return Response(FULFILMENT_SUCCESSFUL.format(reservation_id), status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetTotalMemberDuesView(APIView):
    def get(self, request):
        pass

