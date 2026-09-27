from django import forms
from .models import Delivery
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class DeliveryForm(forms.ModelForm):
    
    class Meta:
        model = Delivery
        fields = ['pickup_address', 'dropoff_address','vehicle_type','notes', 'scheduled_date']
        labels = {
            'pickup_address': 'عنوان الاستلام (من)',
            'dropoff_address': 'عنوان التسليم (إلى)',
            'scheduled_date': 'الميعاد المخطط',
            'vehicle_type': 'نوع المركبة المطلوب' ,
            'notes': 'ملاحظات (اختياري)'
        }
        widgets = {
            'pickup_address': forms.TextInput(
                attrs={'placeholder': 'عنوان الاستلام (من)'}),
            'dropoff_address': forms.TextInput(
                attrs={'placeholder':'عنوان التسليم (إلى)'}),
            'scheduled_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='البريد الإلكتروني')
    name = forms.CharField(label='الاسم بالكامل')
    phone = forms.CharField(label='رقم الموبايل')
    role = forms.ChoiceField(
        label='نوع الحساب',
        choices=[
            ('customer', 'عميل — عايز أطلب شحنات'),
            ('driver', 'سائق — عايز أشيل شحنات'),
        ],
    )
    vehicle_type = forms.ChoiceField(
        label='نوع المركبة (للسائقين فقط)',
        choices=Delivery.VEHICLE_CHOICES,
        required=False,
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'name', 'phone']