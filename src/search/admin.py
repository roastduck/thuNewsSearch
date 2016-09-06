from django.contrib import admin

from .models import Pages
from .models import Inverted

admin.site.register(Pages)
admin.site.register(Inverted)

