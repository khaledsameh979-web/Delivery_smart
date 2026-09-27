from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login  as asauth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required 
from .models import Delivery, Customer, Driver,StatusHistory
from .forms import DeliveryForm, RegisterForm
def index(request):
    return render(request,'delivery/home.html')
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            asauth_login(request, user)
            if user.role == 'driver':
                return redirect('driver_home')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'delivery/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['role'] == 'driver':
                user.role = 'driver'
                user.save()
                Driver.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    phone=form.cleaned_data['phone'],
                    vehicle_type=form.cleaned_data['vehicle_type'] or 'van',
                )
            else:
                Customer.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    phone=form.cleaned_data['phone'],
                    address='')
            asauth_login(request, user)
            if user.role == 'driver':
                return redirect('driver_home')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'delivery/register.html', {'form': form})
@login_required
def add(request):
    if request.user.role != 'customer':
        return redirect('home')
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.customer = request.user.customer
            delivery.save()
            StatusHistory.objects.create(
                delivery=delivery,
                old_status=None,
                new_status='PENDING',
                changed_by=request.user,
            )
            return redirect('/track/?number=' + str(delivery.tracking_number))
    else:
        form = DeliveryForm()
    return render(request, 'delivery/request_shipment.html', {'form': form})
def track(request):
    delivery=None
    number=request.GET.get('number')
    if number:
        delivery=get_object_or_404(Delivery,tracking_number=number)
    return render(request, 'delivery/track.html', {'delivery': delivery})

@login_required
def driver_home(request):
    if request.user.role != 'driver':
        return redirect('home')

    if request.method == 'POST':
        delivery = get_object_or_404(Delivery, id=request.POST.get('delivery_id'), driver=request.user.driver)
        new_status = request.POST.get('new_status')
        if new_status in ['IN_TRANSIT', 'DELIVERED', 'DELAYED'] and new_status != delivery.status:
            StatusHistory.objects.create(
                delivery=delivery,
                old_status=delivery.status,
                new_status=new_status,
                changed_by=request.user,
            )
            delivery.status = new_status
            delivery.save()
        return redirect('driver_home')

    driver = request.user.driver
    deliveries = Delivery.objects.filter(driver=driver).exclude(status='DELIVERED').order_by('scheduled_date')
    return render(request, 'delivery/driver_home.html', {'deliveries': deliveries})




# Create your views here.
