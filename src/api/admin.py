from django.contrib import admin
from .models import PracticeList
from .models import ChatHistory
from .models import PracticeHistory

class PracticeListAdmin(admin.ModelAdmin):
    list_display = ('user', 'words')  # Fields to display in list view
    search_fields = ['user']  # Fields that can be searched

admin.site.register(PracticeList, PracticeListAdmin)

class PracticeHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'words')  # Fields to display in list view
    search_fields = ['user']  # Fields that can be searched

admin.site.register(PracticeHistory, PracticeHistoryAdmin)

class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'chat', 'date')  # Fields to display in list view
    search_fields = ['user']  # Fields that can be searched

admin.site.register(ChatHistory, ChatHistoryAdmin)