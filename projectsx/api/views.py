from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Transcription, Translation, UserAccount, TranscriptionGo, TranslationGo, ContactMessage
import openai
from .serializers import TranscriptionSerializer, TranslationSerializer, TranscriptionGoSerializer, TranslationGoSerializer, ContactMessageSerializer, UserAccountSerializer
from .constants import ApiKeys
from django.conf import settings
from django.http import HttpResponse
import os
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status


class TranscriptionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer

    def create(self, request):
        audio_file = request.FILES['audio']
        response_format = request.POST.get('response_format', 'srt')  # Get the selected response format (default is 'srt')
        transcription_text = openai.Audio.transcribe(
            api_key=ApiKeys.API_KEY,
            model='whisper-1',
            file=audio_file,
            response_format=response_format
        )

        transcription = Transcription(
            audio=audio_file,
            transcription_text=transcription_text,
            user=request.user
        )
        
        transcription.save()

        return Response(transcription.to_json())
    

    def patch(self, request, pk):
        transcription = self.get_object(pk)
        transcription.transcription_text = request.data.get('transcription_text')
        transcription.save()

        return Response(transcription.to_json())

    def list_by_user(self, request, user_id):
        user = get_object_or_404(UserAccount, pk=user_id)
        transcriptions = Transcription.objects.filter(user=user)
        serializer = TranscriptionSerializer(transcriptions, many=True, context={'request': request})

        # Update the audio URLs in the response
        updated_data = []
        for data in serializer.data:
            audio_path = data["audio"]
            audio_url = request.build_absolute_uri(audio_path)
            data["audio"] = audio_url
            updated_data.append(data)

        return Response(updated_data)

    
    @action(detail=False, methods=['GET'])
    def reviewed(self, request):
        transcriptions = Transcription.objects.filter(review=True)
        serializer = TranscriptionSerializer(transcriptions, many=True)
        return Response(serializer.data)
    
    def update_remaining_free_minutes(self, request):
        new_remaining_free_minutes = request.data.get('remaining_free_minutes')

        if new_remaining_free_minutes is None:
            return Response(
                {'detail': 'Please provide the new value for remaining free minutes.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        user.remaining_free_minutes = new_remaining_free_minutes
        user.save()

        return Response(
            {'detail': 'Remaining free minutes updated successfully.'},
            status=status.HTTP_200_OK
        )
    
class TranslationViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer

    def create(self, request):
        audio_file = request.FILES['audio']
        response_format = request.POST.get('response_format', 'srt')  # Get the selected response format (default is 'srt')
        translation_text = openai.Audio.translate(
            api_key=ApiKeys.API_KEY,
            model='whisper-1',
            file=audio_file,
            response_format=response_format
        )

        translation = Translation(
            audio=audio_file,
            translation_text=translation_text,
            user=request.user
        )
        
        translation.save()

        return Response(translation.to_json())
    

    def patch(self, request, pk):
        translation = self.get_object(pk)
        translation.translation_text = request.data.get('transcription_text')
        translation.save()

        return Response(translation.to_json())
    
    def list_by_user(self, request, user_id):
        user = get_object_or_404(UserAccount, pk=user_id)
        translations = Translation.objects.filter(user=user)
        serializer = TranslationSerializer(translations, many=True)
        return Response(serializer.data)
    
class TranscriptionGoViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []

    queryset = TranscriptionGo.objects.all()
    serializer_class = TranscriptionGoSerializer

    def create(self, request):
        audio_file = request.FILES['audio']
        response_format = request.POST.get('response_format', 'srt')  # Get the selected response format (default is 'srt')

        transcription_text = openai.Audio.transcribe(
            api_key=ApiKeys.API_KEY,
            model='whisper-1',
            file=audio_file,
            response_format=response_format  # Pass the selected response format to the transcription method
        )

        transcription = TranscriptionGo(
            audio=audio_file,
            transcription_text=transcription_text
        )
        
        transcription.save()

        return Response(transcription.to_json())
    

    def patch(self, request, pk):
        transcription = self.get_object(pk)
        transcription.transcription_text = request.data.get('transcription_text')
        transcription.save()

        return Response(transcription.to_json())

    
class TranslationGoViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []
    queryset = TranslationGo.objects.all()
    serializer_class = TranslationGoSerializer

    def create(self, request):
        audio_file = request.FILES['audio']
        response_format = request.POST.get('response_format', 'srt')  # Get the selected response format (default is 'srt')
        translation_text = openai.Audio.translate(
            api_key=ApiKeys.API_KEY,
            model='whisper-1',
            file=audio_file,
            response_format=response_format
        )

        translation = TranslationGo(
            audio=audio_file,
            translation_text=translation_text,
        )
        
        translation.save()

        return Response(translation.to_json())
    

    def patch(self, request, pk):
        translation = self.get_object(pk)
        translation.translation_text = request.data.get('transcription_text')
        translation.save()

        return Response(translation.to_json())
    
class TheOfficeViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Transcription.objects.filter(review=True)
    serializer_class = TranscriptionSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer


class UserAccountViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer

    @action(detail=False, methods=['GET'])
    def get_remaining_free_minutes(self, request, user_id):
        user = get_object_or_404(UserAccount, pk=user_id)
        remaining_free_minutes = user.remaining_free_minutes
        return Response({'remainingfreeminutes': remaining_free_minutes})

    @action(detail=False, methods=['POST'])
    def update_remaining_free_minutes(self, request, user_id):
        user = get_object_or_404(UserAccount, pk=user_id)
        remaining_free_minutes = request.data.get('remainingfreeminutes')
        user.remaining_free_minutes = remaining_free_minutes
        user.save()
        return Response({'remainingfreeminutes': remaining_free_minutes})
