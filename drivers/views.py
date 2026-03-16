from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DriverRegistrationForm
from .models import DriverProfile
from accounts.models import UserProfile


@login_required
def become_driver(request):
    if hasattr(request.user, 'driver_profile'):
        messages.info(request, 'You already have a driver profile.')
        return redirect('driver_dashboard')
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.user = request.user
            driver.save()
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.is_driver = True
            profile.save()
            messages.success(request, 'Driver profile submitted! Pending admin verification.')
            return redirect('driver_dashboard')
    else:
        form = DriverRegistrationForm()
    return render(request, 'drivers/become_driver.html', {'form': form})


@login_required
def driver_dashboard(request):
    if not hasattr(request.user, 'driver_profile'):
        return redirect('become_driver')
    driver = request.user.driver_profile
    my_rides = request.user.rides_as_driver.all().order_by('-departure_datetime')
    pending_requests = []
    for ride in my_rides:
        pending_requests.extend(ride.requests.filter(status='pending'))
    return render(request, 'drivers/driver_dashboard.html', {
        'driver': driver,
        'my_rides': my_rides,
        'pending_requests': pending_requests,
    })
