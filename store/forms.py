from django import forms
from django.forms import ModelForm
from .models import User, Order


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'date_of_birth')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password',)


class RegisterForm(ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.CharField(label='Date of birth', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'date_of_birth', 'password1', 'password2',)


class ProfileForm(ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.CharField(label='Date of birth', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Phone number', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   required=False)
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    street = forms.CharField(label='Street', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    house_number = forms.CharField(label='House number', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   required=False)
    zip_code = forms.CharField(label='Zip code', widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=False)

    class Meta:
        model = User
        fields = (
        'username', 'email', 'date_of_birth', 'phone_number', 'country', 'city', 'street',
        'house_number', 'zip_code',)

class OrderForm(ModelForm):
    country_order = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-control'}))
    city_order = forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'form-control'}))
    street_order = forms.CharField(label='Street', widget=forms.TextInput(attrs={'class': 'form-control'}))
    house_number_order = forms.CharField(label='House number', widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip_code_order = forms.CharField(label='Zip code', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email_order = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number_order = forms.CharField(label='Phone number', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ('country_order', 'city_order', 'street_order', 'house_number_order', 'zip_code_order', 'email_order', 'phone_number_order',)