from django.contrib import admin
from .models import Transcription, Translation,TranscriptionGo, TranslationGo, UserAccount, ContactMessage, Feedback, Article
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.
admin.site.register(Transcription)
admin.site.register(Translation)
admin.site.register(UserAccount)
admin.site.register(TranscriptionGo)
admin.site.register(TranslationGo)
admin.site.register(ContactMessage)
admin.site.register(Feedback)

class articleEditorAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

admin.site.register(Article, articleEditorAdmin)