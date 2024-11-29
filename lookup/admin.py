from django.contrib import admin

# Register your models here.
from .models import ContactMessage, Visitor

admin.site.register(ContactMessage)

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'user_agent', 'visited_at', 'url_visited')
    list_filter = ('visited_at',)
    search_fields = ('ip_address', 'user_agent', 'url_visited')