from django.contrib import admin
from .models import Note, Author

# Register your models here.
admin.site.register([Note, Author])
