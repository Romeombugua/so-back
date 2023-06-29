from django.urls import path

from .views import TranscriptionViewSet, TranslationViewSet, TranscriptionGoViewSet, TranslationGoViewSet, TheOfficeViewSet, ContactMessageViewSet

urlpatterns = [
    path('transcripts', TranscriptionViewSet.as_view({
        'get': 'list', 
        'post': 'create'
        })),
    path('transcripts/<int:pk>', TranscriptionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),

    path('transcribego', TranscriptionGoViewSet.as_view({
        'get': 'list', 
        'post': 'create'
        })),
    path('transcribego/<int:pk>', TranscriptionGoViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),
    path('translate', TranslationViewSet.as_view({
        'get': 'list', 
        'post': 'create'
        })),
    path('translate/<int:pk>', TranslationViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),
    path('translatego', TranslationGoViewSet.as_view({
        'get': 'list', 
        'post': 'create'
        })),
    path('translatego/<int:pk>', TranslationGoViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),

    path('transcripts/user/<int:user_id>', TranscriptionViewSet.as_view({
        'get': 'list_by_user'
    })),
    path('translate/user/<int:user_id>', TranslationViewSet.as_view({
        'get': 'list_by_user'
    })),
    path('theoffice', TheOfficeViewSet.as_view({
        'get': 'list', 
        })),
    path('theoffice/<int:pk>', TheOfficeViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'})),
    path('contactus', ContactMessageViewSet.as_view({
        'get': 'list', 
        'post': 'create'
        })),
]