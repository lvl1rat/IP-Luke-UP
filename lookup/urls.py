from django.contrib import admin
from django.urls import path
from lookup.views import ip_lookup  # Import your view
from . import views

urlpatterns = [
    path('', ip_lookup, name='home'),  # Add this for the root URL
    path('lookup/', ip_lookup, name='ip_lookup'),
    path('admin/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]