from django.views.generic import TemplateView
from django.shortcuts import render

class HomeView(TemplateView):
    template_name = 'index.html'

class BranchesView(TemplateView):
    template_name = 'branches.html'

class PackagesView(TemplateView):
    template_name = 'packages.html'

class GalleryView(TemplateView):
    template_name = 'gallery.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

class BookingView(TemplateView):
    template_name = 'booking.html'
