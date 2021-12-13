from django.contrib import admin
from .models import Language, Report, TechContent, TechContentVersion, User, Item

# from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(TechContent)
admin.site.register(TechContentVersion)
admin.site.register(Language)
admin.site.register(Item)
admin.site.register(Report)
