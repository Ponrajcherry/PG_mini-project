from django.urls import path
from .views import HomeView, BranchesView, PackagesView, GalleryView, ContactView, BookingView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('branches/', BranchesView.as_view(), name='branches'),
    path('packages/', PackagesView.as_view(), name='packages'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('booking/', BookingView.as_view(), name='booking'),
]
