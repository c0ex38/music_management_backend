# music/urls.py

from django.urls import path

# Gerekli görünümleri (view) içe aktar
from .views import (
    MusicListCreateView,            # Müzik listesi oluşturma ve görüntüleme
    PlaylistCreateView,              # Çalma listesi oluşturma
    PlaylistDetailView,              # Belirli bir çalma listesinin detaylarını görüntüleme
    PlaylistScheduleListCreateView,  # Çalma listesi zamanlaması oluşturma ve görüntüleme
    MusicUploadView,                 # Müzik dosyası yükleme
    PlayCountStatsView,              # Çalma istatistiklerini görüntüleme
    PlaylistByStoreView,             # Mağazaya göre çalma listelerini görüntüleme
    AnnouncementByStoreView,         # Mağazaya göre anonsları görüntüleme
    PlayHistoryListCreateView        # Çalma geçmişi oluşturma ve görüntüleme
)

urlpatterns = [
    path('music/', MusicListCreateView.as_view(), name='music-list-create'),  # Müzik oluşturma ve listeleme
    path('playlist/', PlaylistCreateView.as_view(), name='playlist-create'),   # Çalma listesi oluşturma
    path('playlist/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),  # Belirli bir çalma listesinin detayları
    path('schedule/', PlaylistScheduleListCreateView.as_view(), name='schedule-list-create'),  # Çalma listesi zamanlaması oluşturma ve listeleme
    path('music/upload/', MusicUploadView.as_view(), name='music-upload'),  # Müzik dosyası yükleme
    path('play-history/', PlayHistoryListCreateView.as_view(), name='play-history'),  # Çalma geçmişi oluşturma ve listeleme
    path('play-count-stats/', PlayCountStatsView.as_view(), name='play-count-stats'),  # Çalma istatistiklerini görüntüleme
    path('playlist/by-store/', PlaylistByStoreView.as_view(), name='playlist-by-store'),  # Mağazaya göre çalma listeleri
    path('announcement/by-store/', AnnouncementByStoreView.as_view(), name='announcement-by-store'),  # Mağazaya göre anonslar
]
