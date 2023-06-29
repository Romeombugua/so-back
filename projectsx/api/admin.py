from django.contrib import admin
from .models import Transcription, Translation,TranscriptionGo, TranslationGo, UserAccount, ContactMessage

# Register your models here.
admin.site.register(Transcription)
admin.site.register(Translation)
admin.site.register(UserAccount)
admin.site.register(TranscriptionGo)
admin.site.register(TranslationGo)
admin.site.register(ContactMessage)