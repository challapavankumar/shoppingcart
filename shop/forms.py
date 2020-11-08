from django.contrib.auth.models import User
from django import forms
from .models import Order,Customer,Product

class ChcekOutForm(forms.ModelForm):

    class Meta:
        model=Order
        fields=['ordered_by','shipping_adress','mobile','email','payment_method']



class CustomerLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))


class CustomerRegisterForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your name'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'******'}))
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'abcd@gmail.com'}))
    class Meta:
        model= Customer
        fields= ['username','password','email','full_name','address']
        widgets={
            'full_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your full name'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your address'}),
        }
    def clean_username(self):
        uname=self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                " Customer with this username already exists.."
            )
        return uname

class AdminLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'********'}))
class AdminAddProductForm(forms.ModelForm):
    more_images=forms.FileField(required=False,widget=forms.FileInput(attrs={'class':'form-control','multiple':True}))
    class Meta:
        model=Product
        fields=['title','slug','category',
                'image','marked_price','selling_price',
                'description','warranty','return_policy']

        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter title'}),
            'slug':forms.TextInput(attrs={'class':'form-control','placeholder':'abcd-cd..'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'select category'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'upload images'}),
            'marked_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'marked price of the product'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'selling price of the product '}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description of the product'}),
            'warranty': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'warrany of the product '}),
            'return_policy': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'return policy  of the product'}),
        }
class PasswordForgeForm(forms.Form):
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Abc@gmail.com'}))


    def clean_email(self):
        e=self.cleaned_data.get('email')
        if Customer.objects.filter(user__email=e).exists():


            pass
        else:
            raise forms.ValidationError('error email..')
        return e

class Password_Reset_Form(forms.Form):
    new_password=forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control',
               'autocomplete':'new_password',
               'placeholder':'enter  New password',

               }),label="new password"
    )
    confirm_new_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new_password',
        'placeholder': 'confirm  New password',

    }), label="confirm new password"
    )
    def clean_confirm_new_password(self):
        new_password=self.cleaned_data.get('new_password')
        confirm_new_password=self.cleaned_data.get('confirm_new_password')
        if new_password  != confirm_new_password:
            raise forms.ValidationError(
                'new password did not match'
            )

