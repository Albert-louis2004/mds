

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views  # Importă direct `views`, fără importuri individuale
from django.contrib.auth import views as auth_views

app_name = 'store'  # Namespace corect

urlpatterns = [
    path('',views.home,name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('message/', views.contact_thank_you_view, name='contact_thank_you'),
    path('adauga_produs/', views.adauga_produs, name='adauga_produs'),
    path('registration/', views.register, name='register'),
    path('cart/', views.cart_detail, name='cart_detail'),  # Coș de cumpărături
    path('cart/add/<int:laptop_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('registration/login/', auth_views.LoginView.as_view(), name='login'),
    path('registration/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]

# Servirea fișierelor statice și media în timpul dezvoltării
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])



