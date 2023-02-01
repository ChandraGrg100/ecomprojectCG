from django.shortcuts import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth import authenticate,login
from .models import UserCreateFrom





# Create your views here.

def base(request):
    return render(request,"base.html")

def Index(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(subcategory=categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')

    else:
        product = Product.objects.all()
    context = {
        "category":category,
        "product":product,
        "brand":brand,
    }
    return render(request, "index.html", context)

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password= form.cleaned_data['password1'],
            )
            login(request,new_user)
            return HttpResponseRedirect("index")
    else:
        form = UserCreateFrom()
    context = {
        "form":form,
    }
    return render(request,"registration/signup.html",context)

@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

def Contact(request):
    if request.method == "POST":
        contact = Contact_us(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )
        contact.save()
    return render(request,'contact.html')

def CheckOut(request):
    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        pincode = request.POST.get("pincode")
        cart = request.session.get('cart')
        uid= request.session.get('_auth_user_id')
        user = User.objects.get(pk= uid)
        print(cart)

        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a * b
            order = Order(
                user = user,
                product = cart[i]["name"],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                image = cart[i]['image'],
                address = address,
                phone = phone,
                pincode = pincode,
                total = total,
            )
            order.save()
        request.session['cart'] = {}  #clear cart after checkout
        return redirect('index')

def YourOrder(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)

    order = Order.objects.filter(user=user)
    context ={
        'order':order,
    }

    return render(request,'order.html',context)

def Shop(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(subcategory=categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all()

    context= {
        'category':category,
        'brand':brand,
        'product':product,
    }
    return render(request,"shop.html",context)

def ProductDetail(request,id):
    product = Product.objects.filter(id=id).first()
    context = {
        "product":product
    }
    return render(request,'product-details.html',context)

def Search(request):
    query = request.GET['query']
    product = Product.objects.filter(name__icontains=query)
    brand = Brand.objects.filter(name__icontains=query)
    context = {
        'product':product,
        'brand':brand,
    }
    return render(request,'search.html',context)