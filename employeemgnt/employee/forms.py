from django import forms
from employee.models import EmployeeInfo, EmployeeAddress

# Create your models here.
class EmployeeInfoForm(forms.ModelForm):
    class Meta:
        model = EmployeeInfo
        exclude = ['employeeAddress']
        widgets = {
            'gender': forms.RadioSelect
        }
        labels = {
            'bloodGroup': 'Blood Group'
        }
class EmployeeAddressForm(forms.ModelForm):
    class Meta:
        model = EmployeeAddress
        exclude = ['employeeInfo']
        labels = {
            'addressLine1': 'Address Line 1',
            'addressLine2': 'Address Line 2',
        }
