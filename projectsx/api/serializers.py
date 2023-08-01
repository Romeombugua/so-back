from rest_framework import serializers
from .models import Transcription, Translation, TranscriptionGo, TranslationGo, ContactMessage, UserAccount, Feedback, Article
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class TranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcription
        fields = ('id', 'name', 'user', 'audio', 'transcription_text', 'transcription_file', 'review')

class TranscriptionGoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionGo
        fields = ('id', 'audio', 'transcription_text', 'transcription_file')
class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ('id','name', 'user', 'audio', 'translation_text', 'translation_file')

class TranslationGoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationGo
        fields = ('id', 'audio', 'translation_text', 'translation_file')


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id','remaining_free_minutes')

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'