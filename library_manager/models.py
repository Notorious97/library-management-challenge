from django.db import models

from library_manager.constants import ALREADY_RETURNED, BOOK_DOESNT_EXIST, BOOK_NOT_AVAILABLE, CHECKOUT_NOT_AVAILABLE, MEMBER_DOESNT_EXIST, RESERVATION_ALREADY_CREATED, RESERVATION_NOT_PRESENT

# Create your models here.

class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500)
    copies = models.IntegerField(default=0)
    
    
class Member(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500)
    
    
class Circulation(models.Model):
    id = models.BigAutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True)
    checked_out_at = models.DateTimeField(help_text="Datetime at which the book was checked out by the member")
    returned_at = models.DateTimeField(help_text="Datetime at which the book was returned by the member", blank=True, null=True)
    
    
    @classmethod
    def checkout_book(cls, book_id, member_id, date):
        book = Book.objects.filter(id=book_id).first()
        member = Member.objects.filter(id=member_id).first()
        
        if not book:
            return None, BOOK_DOESNT_EXIST, False
        elif not member:
            return None, MEMBER_DOESNT_EXIST, False
        
        if book.copies <= 0:
            return Reservation.reserve_book(book_id, member_id, date)
        
        circulation = cls.objects.create(book_id=book_id, member_id=member_id, checked_out_at=date)
        book.copies = book.copies - 1
        book.save()
        return circulation.id, None, False
        
    @classmethod
    def return_book(cls, book_id, member_id, date):
        book = Book.objects.filter(id=book_id).first()
        member = Member.objects.filter(id=member_id).first()
        
        if not book:
            return None, BOOK_DOESNT_EXIST
        elif not member:
            return None, MEMBER_DOESNT_EXIST
        
        
        circulation = cls.objects.filter(book_id=book_id, member_id=member_id).first()
        if not circulation:
            None, CHECKOUT_NOT_AVAILABLE
        elif circulation.returned_at:
            None, ALREADY_RETURNED
            
        circulation.returned_at = date
        book.copies += 1
        book.save()
        circulation.save()
        
        return circulation.id, None
    


class Reservation(models.Model):
    id = models.BigAutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True)
    reserved_at = models.DateTimeField(help_text="Datetime at which the book was reserved by the member")
    fulfilled_at = models.DateTimeField(help_text="Datetime at which the reservation was fulfilled", blank=True, null=True)
    
    
    @classmethod
    def reserve_book(cls, book_id, member_id, date):
        
        old_reservation = cls.objects.filter(member_id=member_id, book_id=book_id).order_by("-reserved_at").first()
        if old_reservation and old_reservation.fulfilled_at is None:
            return None, RESERVATION_ALREADY_CREATED.format(old_reservation.book_id), False
        
        reservation = cls.objects.create(book_id=book_id, member_id=member_id, reserved_at=date)
        return reservation.id, None, True
    
    @classmethod
    def fulfil_book(cls, book_id, date):
        book = Book.objects.filter(id=book_id).first()
        
        if not book:
            return None, BOOK_DOESNT_EXIST
        
        
        reservation = cls.objects.filter(book_id=book_id, fulfilled_at__isnull=True).order_by("reserved_at")
        if not reservation.exists():
            None, RESERVATION_NOT_PRESENT

        try:
            reservation = reservation.first()
            reservation.fulfilled_at = date
            reservation.save()
            
        except AttributeError:
            return None, RESERVATION_NOT_PRESENT
        
        return reservation.id, None
    
