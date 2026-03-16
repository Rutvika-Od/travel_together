from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from .models import Ride, RideRequest, RideMessage, Notification
from .forms import RideForm, RideRequestForm, MessageForm, SearchForm
from accounts.models import UserProfile


def home(request):
    recent_rides = Ride.objects.filter(
        status='active',
        departure_datetime__gte=timezone.now()
    ).select_related('driver__profile', 'driver__driver_profile').order_by('departure_datetime')[:6]
    search_form = SearchForm()
    total_rides = Ride.objects.filter(status='active').count()
    total_drivers = Ride.objects.values('driver').distinct().count()
    popular_routes = Ride.objects.filter(
        status='active', departure_datetime__gte=timezone.now()
    ).values('start_city', 'destination_city').distinct()[:6]
    return render(request, 'home.html', {
        'recent_rides': recent_rides,
        'search_form': search_form,
        'total_rides': total_rides,
        'total_drivers': total_drivers,
        'popular_routes': popular_routes,
    })


@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    my_requests = request.user.ride_requests.select_related('ride__driver').order_by('-requested_at')
    upcoming_rides = my_requests.filter(status='approved', ride__departure_datetime__gte=timezone.now())
    driver_profile = getattr(request.user, 'driver_profile', None)
    my_rides = request.user.rides_as_driver.all().order_by('-departure_datetime') if driver_profile else []
    notifications = request.user.ride_notifications.filter(is_read=False)[:5]
    return render(request, 'dashboard.html', {
        'profile': profile,
        'driver_profile': driver_profile,
        'my_requests': my_requests[:5],
        'upcoming_rides': upcoming_rides,
        'my_rides': my_rides[:5],
        'notifications': notifications,
    })


@login_required
def search_rides(request):
    form = SearchForm(request.GET)
    rides = Ride.objects.filter(status='active', departure_datetime__gte=timezone.now())
    if form.is_valid():
        start = form.cleaned_data.get('start_city')
        dest = form.cleaned_data.get('destination_city')
        date = form.cleaned_data.get('date')
        seats = form.cleaned_data.get('seats')
        if start:
            rides = rides.filter(start_city__icontains=start)
        if dest:
            rides = rides.filter(destination_city__icontains=dest)
        if date:
            rides = rides.filter(departure_datetime__date=date)
        if seats:
            rides = rides.filter(available_seats__gte=seats)
    rides = rides.select_related('driver__profile', 'driver__driver_profile').order_by('departure_datetime')
    return render(request, 'rides/search_rides.html', {'form': form, 'rides': rides, 'count': rides.count()})


@login_required
def ride_detail(request, pk):
    ride = get_object_or_404(Ride, pk=pk)
    user_request = None
    is_driver = ride.driver == request.user
    can_chat = is_driver

    if not is_driver:
        user_request = RideRequest.objects.filter(ride=ride, passenger=request.user).first()
        if user_request and user_request.status == 'approved':
            can_chat = True

    chat_messages = []
    message_form = MessageForm()

    if can_chat:
        chat_messages = ride.messages.select_related('sender').all()
        if request.method == 'POST':
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                msg = message_form.save(commit=False)
                msg.ride = ride
                msg.sender = request.user
                msg.save()
                if not is_driver:
                    Notification.objects.create(
                        user=ride.driver, notif_type='new_message',
                        message=f'{request.user.get_full_name() or request.user.username} sent a message.',
                        link=f'/rides/{ride.pk}/'
                    )
                return redirect('ride_detail', pk=pk)

    approved_passengers = ride.requests.filter(status='approved').select_related('passenger__profile')
    pending_requests = ride.requests.filter(status='pending').select_related('passenger__profile') if is_driver else []

    return render(request, 'rides/ride_detail.html', {
        'ride': ride,
        'user_request': user_request,
        'is_driver': is_driver,
        'can_chat': can_chat,
        'chat_messages': chat_messages,
        'message_form': message_form,
        'approved_passengers': approved_passengers,
        'pending_requests': pending_requests,
    })


@login_required
def create_ride(request):
    driver = getattr(request.user, 'driver_profile', None)
    if not driver:
        messages.error(request, 'You need to register as a driver first.')
        return redirect('become_driver')
    if not driver.is_verified():
        messages.warning(request, 'Your driver profile is pending verification. You can post rides after admin approval.')
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.driver = request.user
            ride.save()
            messages.success(request, f'Ride posted! {ride.start_city} → {ride.destination_city} 🚗')
            return redirect('ride_detail', pk=ride.pk)
    else:
        form = RideForm()
    return render(request, 'rides/create_ride.html', {'form': form})


@login_required
def edit_ride(request, pk):
    ride = get_object_or_404(Ride, pk=pk, driver=request.user)
    if request.method == 'POST':
        form = RideForm(request.POST, instance=ride)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ride updated!')
            return redirect('ride_detail', pk=pk)
    else:
        form = RideForm(instance=ride)
    return render(request, 'rides/create_ride.html', {'form': form, 'edit': True, 'ride': ride})


@login_required
def delete_ride(request, pk):
    ride = get_object_or_404(Ride, pk=pk, driver=request.user)
    if request.method == 'POST':
        ride.delete()
        messages.success(request, 'Ride deleted.')
        return redirect('driver_dashboard')
    return render(request, 'rides/confirm_delete.html', {'ride': ride})


@login_required
def request_ride(request, pk):
    ride = get_object_or_404(Ride, pk=pk)
    if ride.driver == request.user:
        messages.error(request, "You can't request your own ride.")
        return redirect('ride_detail', pk=pk)
    if ride.is_full():
        messages.error(request, 'This ride is full.')
        return redirect('ride_detail', pk=pk)
    existing = RideRequest.objects.filter(ride=ride, passenger=request.user).first()
    if existing:
        messages.info(request, f'Your request is already {existing.status}.')
        return redirect('ride_detail', pk=pk)
    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.ride = ride
            req.passenger = request.user
            req.save()
            Notification.objects.create(
                user=ride.driver, notif_type='ride_request',
                message=f'{request.user.get_full_name() or request.user.username} wants to join your ride to {ride.destination_city}.',
                link=f'/rides/{ride.pk}/'
            )
            messages.success(request, 'Ride request sent! Waiting for driver approval.')
            return redirect('ride_detail', pk=pk)
    else:
        form = RideRequestForm()
    return render(request, 'rides/request_ride.html', {'ride': ride, 'form': form})


@login_required
def cancel_request(request, pk):
    ride_request = get_object_or_404(RideRequest, pk=pk, passenger=request.user)
    if ride_request.status == 'approved':
        ride_request.ride.available_seats += ride_request.seats_requested
        ride_request.ride.save()
    ride_request.status = 'cancelled'
    ride_request.save()
    messages.success(request, 'Request cancelled.')
    return redirect('dashboard')


@login_required
def manage_requests(request, pk):
    ride = get_object_or_404(Ride, pk=pk, driver=request.user)
    pending = ride.requests.filter(status='pending').select_related('passenger__profile')
    approved = ride.requests.filter(status='approved').select_related('passenger__profile')
    rejected = ride.requests.filter(status='rejected').select_related('passenger__profile')
    return render(request, 'rides/manage_requests.html', {
        'ride': ride, 'pending': pending, 'approved': approved, 'rejected': rejected
    })


@login_required
def update_request(request, pk, req_id, action):
    ride = get_object_or_404(Ride, pk=pk, driver=request.user)
    ride_request = get_object_or_404(RideRequest, pk=req_id, ride=ride)

    if action == 'approve':
        if ride.available_seats >= ride_request.seats_requested:
            ride_request.status = 'approved'
            ride_request.save()
            ride.available_seats -= ride_request.seats_requested
            if ride.available_seats == 0:
                ride.status = 'full'
            ride.save()
            Notification.objects.create(
                user=ride_request.passenger, notif_type='request_approved',
                message=f'Your ride request to {ride.destination_city} was approved! 🎉',
                link=f'/rides/{ride.pk}/'
            )
            messages.success(request, f'Request approved for {ride_request.passenger.get_full_name() or ride_request.passenger.username}!')
        else:
            messages.error(request, 'Not enough available seats.')
    elif action == 'reject':
        ride_request.status = 'rejected'
        ride_request.save()
        Notification.objects.create(
            user=ride_request.passenger, notif_type='request_rejected',
            message=f'Your ride request to {ride.destination_city} was not approved.',
            link=f'/rides/'
        )
        messages.info(request, 'Request rejected.')
    return redirect('manage_requests', pk=pk)


@login_required
def my_rides(request):
    as_passenger = request.user.ride_requests.select_related('ride__driver__profile').order_by('-requested_at')
    as_driver = request.user.rides_as_driver.all().order_by('-departure_datetime') if hasattr(request.user, 'driver_profile') else []
    return render(request, 'rides/my_rides.html', {'as_passenger': as_passenger, 'as_driver': as_driver})


@login_required
def notifications_view(request):
    notifs = request.user.ride_notifications.all()
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'rides/notifications.html', {'notifications': notifs})


def get_unread_count(request):
    if request.user.is_authenticated:
        count = request.user.ride_notifications.filter(is_read=False).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})
