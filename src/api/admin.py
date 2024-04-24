from django.contrib import admin
from .models import PracticeList
from .models import ChatHistory
from .models import PracticeHistory
from .models import Questionnaire

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

class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_year', 'native_language', 'years_speaking_english')  # Fields to display in list view
    search_fields = ['user']  # Fields that can be searched

admin.site.register(Questionnaire, QuestionnaireAdmin)
