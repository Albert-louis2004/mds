from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Laptop, Cart, CartItem
from .forms import ContactForm, LaptopForm, UserRegistrationForm

@login_required
def get_cart(request):
    """Obține coșul utilizatorului curent."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return cart

@login_required
def add_to_cart(request, laptop_id):
    """Adaugă un produs în coș."""
    laptop = get_object_or_404(Laptop, id=laptop_id)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, laptop=laptop)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('store:cart_detail')  # Folosește namespace-ul corect

@login_required
def remove_from_cart(request, item_id):
    """Șterge un produs din coș."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('store:cart_detail')

@login_required
def cart_detail(request):
    """Afișează detaliile coșului de cumpărături."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.laptop.price * item.quantity for item in cart_items)

    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

def home(request):
    """Afișează lista de laptopuri disponibile."""
    laptops = Laptop.objects.all()
    paginator = Paginator(laptops, 10)  # Afișează 10 laptopuri pe pagină
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj})

def adauga_produs(request):
    """Permite utilizatorilor să adauge un produs nou."""
    if request.method == 'POST':
        form = LaptopForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store:home')
    else:
        form = LaptopForm()

    return render(request, 'adauga_produs.html', {'form': form})

def contact_view(request):
    """Formular de contact."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f"Nou mesaj de la {form.cleaned_data['nume']}"
            message = form.cleaned_data['mesaj']
            send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL])
            return redirect('store:contact_thank_you')  # Corectat
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})

def contact_thank_you_view(request):
    """Pagina de mulțumire după trimiterea unui mesaj."""
    return render(request, 'message/contact_thank_you.html')

def send_welcome_email(user_email):
    """Trimite un email de bun venit utilizatorului nou înregistrat."""
    subject = 'Bine ați venit pe site-ul nostru!'
    message = 'Vă mulțumim pentru înregistrare. Ne bucurăm că vă avem alături.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])

def register(request):
    """Înregistrarea unui utilizator nou."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('store:home')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def product_detail(request, pk):
    """Detaliile unui produs individual."""
    product = get_object_or_404(Laptop, pk=pk)
    return render(request, 'product/product_detail.html', {'product': product})

@login_required
def custom_logout(request):
    """Logout utilizator și redirecționare către pagina principală."""
    logout(request)
    return redirect('store:login')  # Corectat