from django.contrib import admin
from .models import Profile,Userpost,Comments
# Register your models here.

admin.site.register(Profile)
admin.site.register(Userpost)
admin.site.register(Comments)