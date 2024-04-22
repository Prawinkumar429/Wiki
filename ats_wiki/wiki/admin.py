from django.contrib import admin
from .models import Wiki,FileUpload,CustomUser



admin.site.register(Wiki)

admin.site.register(FileUpload)

admin.site.register(CustomUser)