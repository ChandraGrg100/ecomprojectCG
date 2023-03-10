from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django import forms
import datetime


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    Availability = (('In stock','In stock'),('Out of Stock','Out of Stock'))
    Condition = (('New','New'),('Like New','Like New'),('Used','Used'))

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, default='')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=False, default='')
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='ecommerce/pimg')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    Availability = models.CharField(choices=Availability, null=True, max_length=100)
    Condition = models.CharField(choices=Condition, null=True, max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserCreateFrom(UserCreationForm):
    email = forms.EmailField(required=True,label="Email",error_messages={'exists':'This Email already exist'})
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super(UserCreateFrom, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


    def save(self,commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data('email')
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_message['exists'])
        return self.cleaned_data['email']

class Contact_us(models.Model):
    name= models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    subject= models.CharField(max_length=100)
    message= models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    image = models.ImageField(upload_to='ecommerce/order/image')
    product = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.CharField(max_length=5)
    total = models.CharField(max_length=10000, default='')
    address = models.TextField()
    phone = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10)
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.product

