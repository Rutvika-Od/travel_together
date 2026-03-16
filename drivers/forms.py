from django import forms
from .models import DriverProfile


class DriverRegistrationForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['license_number', 'license_image', 'car_model', 'car_number', 'car_color',
                  'car_rc_document', 'insurance_document']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'form-control'})
        self.fields['license_image'].widget.attrs.update({'accept': 'image/*'})
        self.fields['car_rc_document'].widget.attrs.update({'accept': '.pdf,image/*'})
        self.fields['insurance_document'].widget.attrs.update({'accept': '.pdf,image/*'})
