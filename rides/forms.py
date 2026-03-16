from django import forms
from .models import Ride, RideMessage, RideRequest


class RideForm(forms.ModelForm):
    departure_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Ride
        fields = ['start_city', 'destination_city', 'departure_datetime',
                  'price_per_seat', 'total_seats', 'available_seats',
                  'pickup_points', 'drop_points', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, f in self.fields.items():
            if 'class' not in f.widget.attrs:
                f.widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        self.fields['pickup_points'].widget.attrs['placeholder'] = 'e.g. Palanpur Bus Stand, Railway Station'
        self.fields['drop_points'].widget.attrs['placeholder'] = 'e.g. Mehsana GSRTC, Civil Hospital'


class RideRequestForm(forms.ModelForm):
    class Meta:
        model = RideRequest
        fields = ['seats_requested', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'form-control',
                                             'placeholder': 'Introduce yourself to the driver...'}),
            'seats_requested': forms.Select(choices=[(i, i) for i in range(1, 5)],
                                            attrs={'class': 'form-control'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = RideMessage
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type a message...',
                'autocomplete': 'off'
            })
        }
        labels = {'message': ''}


class SearchForm(forms.Form):
    start_city = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'From City'})
    )
    destination_city = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To City'})
    )
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    seats = forms.IntegerField(
        required=False, min_value=1, max_value=6,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Seats', 'min': 1, 'max': 6})
    )
