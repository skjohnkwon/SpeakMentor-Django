from django.contrib import admin
from .models import UserData
from .models import PracticeList
from .models import ChatHistory
from .models import PracticeHistory

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'sub_plan', 'practice_list', 'chat_history')  # Fields to display in list view
    search_fields = ['user']  # Fields that can be searched

admin.site.register(UserData, UserDataAdmin)


class PracticeListAdmin(admin.ModelAdmin):
    list_display = ('user', 'words')  # Fields to display in list view
    search_fields = ['user']  # Fields that can be searched

admin.site.register(PracticeList, PracticeListAdmin)


class PracticeHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'words')  # Fields to display in list view
    search_fields = ['user']  # Fields that can be searched

admin.site.register(PracticeHistory, PracticeHistoryAdmin)


class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat', 'date')  # Fields to display in list view
    search_fields = ['user']  # Fields that can be searched

admin.site.register(ChatHistory, ChatHistoryAdmin)