from django.contrib import admin
from .models import Word

# Register your models here.

class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'laymans')  # Fields to display in list view
    search_fields = ('word',)  # Fields that can be searched

# Register your models here.
admin.site.register(Word, WordAdmin)

from django.contrib import admin
from django.contrib.sessions.models import Session
from django.utils.safestring import mark_safe
import json

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'get_data', 'expire_date']
    readonly_fields = ['session_key', 'get_data', 'expire_date']
    exclude = ['session_data']
    
    def get_data(self, obj):
        # Helper function to deserialize the session data
        return mark_safe(f"<pre>{json.dumps(obj.get_decoded(), indent=4)}</pre>")
    get_data.short_description = 'Session Data'

    def has_add_permission(self, request):
        # Disable adding new sessions through admin
        return False

    def has_change_permission(self, request, obj=None):
        # Disable modifying sessions through admin
        return False