from django.contrib import admin
from .models import Partner


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'google_doc_id')


admin.site.register(Partner, ProfileAdmin)
