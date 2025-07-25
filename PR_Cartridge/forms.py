# PC_Permission/forms.py

from django import forms
from .models import CartridgeRequest
from .models import MISAsset
class CartridgeRequestForm(forms.ModelForm):
    class Meta:
        model = CartridgeRequest
        fields = [
            'printer_no',
            'employee_no',
            'employee_name',
            'designation',
            'department',
            'contact_no',
            'usage_status',
            'hod_name',
        ]
        widgets = {
            'printer_no': forms.TextInput(attrs={'class': 'design'}),
            'employee_no': forms.TextInput(attrs={'class': 'design'}),
            'employee_name': forms.TextInput(attrs={'class': 'design'}),
            'designation': forms.TextInput(attrs={'class': 'design'}),
            'department': forms.TextInput(attrs={'class': 'design'}),
            'contact_no': forms.TextInput(attrs={'class': 'design'}),
            'usage_status': forms.Select(attrs={'class': 'design'}),
            'hod_name': forms.TextInput(attrs={'class': 'design'}),
        }

    def __init__(self, *args, **kwargs):
        # Pop out the employee if provided
        self.employee = kwargs.pop('employee', None)
        super().__init__(*args, **kwargs)

    def clean_printer_no(self):
        printer_no = self.cleaned_data['printer_no'].strip()
        try:
            asset = MISAsset.objects.get(printer_no=printer_no)
        except MISAsset.DoesNotExist:
            raise forms.ValidationError("Invalid printer number. Please enter a valid printer.")
        return printer_no
    def clean(self):
        cleaned_data = super().clean()
        usage_status = cleaned_data.get('usage_status')
        hod_name = cleaned_data.get('hod_name')

        if usage_status == 'Common Employee' and not hod_name:
            self.add_error('hod_name', 'HOD Name is required for Common Employee usage.')

        return cleaned_data

