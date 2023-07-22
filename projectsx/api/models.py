from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.conf import settings
# Create your models here.

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    remaining_free_minutes = models.FloatField(default=12.0)  # New field to store remaining free minutes

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email

class Transcription(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, default=1, blank=True)
    audio = models.FileField(upload_to='audio/transcribe/')
    transcription_text = models.TextField(blank=True)
    transcription_file = models.FileField(upload_to='transcripts/', blank=True)
    name = models.CharField(max_length=255, blank=True)  # New name field
    review = models.BooleanField(default=False)

    # Add any additional fields you may need

    def __str__(self):
        return f'Transcription {self.id}'

    def save(self, *args, **kwargs):
        if not self.name:
            # Get the original file name from the audio field
            audio_file_name = os.path.basename(self.audio.name)
            
            # Set the name field to the audio file name
            self.name = os.path.splitext(audio_file_name)[0]
            
        if self.transcription_text and not self.transcription_file:
            # Generate the file name for the text file based on the name field
            text_file_name = self.name + '.txt'
            
            # Construct the directory path within the 'media' directory
            directory_path = os.path.join(settings.MEDIA_ROOT, 'transcripts')
            
            # Create the directory if it doesn't exist
            os.makedirs(directory_path, exist_ok=True)

            # Construct the file path within the 'transcripts' directory
            file_path = os.path.join(directory_path, text_file_name)

            # Check if the text file already exists
            if not os.path.exists(file_path):
                # Write the transcription_text to the text file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.transcription_text)

                # Open the saved text file and assign it to the transcription_file field
                with open(file_path, 'rb') as file:
                    content = file.read()
                    self.transcription_file.save(text_file_name, ContentFile(content))
                print(file_path)

        super().save(*args, **kwargs)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'audio': self.audio.url,
            'transcription_text': self.transcription_text,
            'transcription_file': self.transcription_file.url if self.transcription_file else None,
        }


class Translation(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, default=1, blank=True)
    audio = models.FileField(upload_to='audio/translate/')
    name = models.CharField(max_length=255, blank=True)
    translation_text = models.TextField(blank=True)
    translation_file = models.FileField(upload_to='translations/', blank=True)
    # Add any additional fields you may need

    def __str__(self):
        return f'Translation {self.id}'

    def save(self, *args, **kwargs):
        if not self.name:
            # Get the original file name from the audio field
            audio_file_name = os.path.basename(self.audio.name)
            self.name = os.path.splitext(audio_file_name)[0]

        if self.translation_text and not self.translation_file:
            # Generate the file name for the text file
            text_file_name = self.name + '.txt'
            
            # Construct the directory path within the 'media' directory
            directory_path = os.path.join(settings.MEDIA_ROOT, 'translations')
            
            # Create the directory if it doesn't exist
            os.makedirs(directory_path, exist_ok=True)

            # Construct the file path within the 'transcripts' directory
            file_path = os.path.join(directory_path, text_file_name)

            # Check if the text file already exists
            if not os.path.exists(file_path):
                # Write the transcription_text to the text file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.translation_text)

                # Open the saved text file and assign it to the transcription_file field
                with open(file_path, 'rb') as file:
                    content = file.read()
                    self.translation_file.save(text_file_name, ContentFile(content))

        super().save(*args, **kwargs)

    def to_json(self):
        return {
            'id': self.id,
            'audio': self.audio.url,
            'name': self.name,
            'translation_text': self.translation_text,
            'translation_file': self.translation_file.url if self.translation_file else None,
        }

    

class TranscriptionGo(models.Model):
    audio = models.FileField(upload_to='audio/transcribe/')
    transcription_text = models.TextField(blank=True)
    transcription_file = models.FileField(upload_to='transcripts/', blank=True)
    # Add any additional fields you may need

    def __str__(self):
        return f'Transcription {self.id}'

    def save(self, *args, **kwargs):
        if self.transcription_text and not self.transcription_file:
            # Get the original file name from the audio field
            audio_file_name = os.path.basename(self.audio.name)
            
            # Generate the file name for the text file
            text_file_name = os.path.splitext(audio_file_name)[0] + '.txt'
            
            # Construct the directory path within the 'media' directory
            directory_path = os.path.join(settings.MEDIA_ROOT, 'transcripts')
            
            # Create the directory if it doesn't exist
            os.makedirs(directory_path, exist_ok=True)

            # Construct the file path within the 'transcripts' directory
            file_path = os.path.join(directory_path, text_file_name)

            # Check if the text file already exists
            if not os.path.exists(file_path):
                # Write the transcription_text to the text file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.transcription_text)

                # Open the saved text file and assign it to the transcription_file field
                with open(file_path, 'rb') as file:
                    content = file.read()
                    self.transcription_file.save(text_file_name, ContentFile(content))
                print(file_path)

        super().save(*args, **kwargs)
        
    def to_json(self):
        return {
            'id': self.id,
            'audio': self.audio.url,
            'transcription_text': self.transcription_text,
            'transcription_file': self.transcription_file.url if self.transcription_file else None,
        }


class TranslationGo(models.Model):
    audio = models.FileField(upload_to='audio/translate/')
    translation_text = models.TextField(blank=True)
    translation_file = models.FileField(upload_to='translations/', blank=True)
    # Add any additional fields you may need

    def __str__(self):
        return f'Translation {self.id}'

    def save(self, *args, **kwargs):
        if self.translation_text and not self.translation_file:
            # Get the original file name from the audio field
            audio_file_name = os.path.basename(self.audio.name)
            
            # Generate the file name for the text file
            text_file_name = os.path.splitext(audio_file_name)[0] + '.txt'
            
            # Construct the directory path within the 'media' directory
            directory_path = os.path.join(settings.MEDIA_ROOT, 'translations')
            
            # Create the directory if it doesn't exist
            os.makedirs(directory_path, exist_ok=True)

            # Construct the file path within the 'transcripts' directory
            file_path = os.path.join(directory_path, text_file_name)

            # Check if the text file already exists
            if not os.path.exists(file_path):
                # Write the transcription_text to the text file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.translation_text)

                # Open the saved text file and assign it to the transcription_file field
                with open(file_path, 'rb') as file:
                    content = file.read()
                    self.translation_file.save(text_file_name, ContentFile(content))
                print(file_path)

        super().save(*args, **kwargs)

    def to_json(self):
        return {
            'id': self.id,
            'audio': self.audio.url,
            'translation_text': self.translation_text,
            'translation_file': self.translation_file.url if self.translation_file else None,
        }
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    large_project = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name