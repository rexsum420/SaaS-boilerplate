from django.contrib import admin
from .models import Order, LineItem

admin.site.register([Order, LineItem])