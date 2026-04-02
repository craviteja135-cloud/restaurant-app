from django.shortcuts import render, redirect
from .models import Contact, MenuItem, Reservation
from django.db.models import Q
import razorpay
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import MenuItemSerializer,ReservationSerializer
from .models import MenuItem
# Create your views here.

def home(request):
    return render(request, "home.html")

def menu(request):
    return render(request, "menu.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
        
        
        return redirect("/contact/?success=1")
        
    success = request.GET.get('success')

    return render(request, "contact.html", {'success': success})

def menu(request):
    items = MenuItem.objects.all()
    return render(request, "menu.html", {'items': items})

def reservation(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        date = request.POST.get("date")
        time = request.POST.get("time")
        guests = request.POST.get("guests")

        already_exists = Reservation.objects.filter(
            date=date,
            time=time,
        ).exists()

        if already_exists:
            return redirect('/reservation/?error=1')
            
        
        Reservation.objects.create(
            name=name,
            phone=phone,
            email=email,
            date=date,
            time=time,
            guests=guests
        )
         
        return redirect("/reservation/?success=1")
    
    success = request.GET.get('success')
    error = request.GET.get('error')
    
    
    return render(request, "reservation.html",{'success': success, 'error': error})

def menu(request):
    search = request.GET.get("search")
    items = MenuItem.objects.all()

    if search:
        items = items.filter(
            Q(name__icontains=search) |
            Q(category__icontains=search) 
        )

    return render(request, "menu.html", {"items": items, "search": search})

def payment_page(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

    item_id = request.GET.get("item_id") 
    
    item = MenuItem.objects.get(id=item_id)
    
    amount = item.price

    razorpay_amount = amount * 100
    display_amount = amount

    payment = client.order.create({
        "amount": razorpay_amount,
        "currency": "INR",
        "receipt": "order_001",
        "payment_capture": 1
    })

    context = {
        "key": settings.RAZORPAY_KEY_ID,
        "amount": razorpay_amount,
        "display_amount": display_amount,
        "order_id": payment["id"],
    }

    return render(request, "payment.html", context)

def payment_success(request):
    return render(request, "payment_success.html")


@api_view(['GET', 'POST'])
def menu_api(request):
    if request.method == "GET":
        items = MenuItem.objects.all()
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = MenuItemSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def reservation_api(request):
    if request.method == "GET":
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ReservationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    