from django.urls import path
from library_manager.views import CheckoutBookView,  FulfillBookView, ReturnBookView, GetTotalMemberDuesView

urlpatterns = [
    path("checkout-book", CheckoutBookView.as_view()),
    path("return-book", ReturnBookView.as_view()),
    path("fulfill-book", FulfillBookView.as_view()),
]