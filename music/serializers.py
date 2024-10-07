# music/serializers.py

from rest_framework import serializers
from .models import Music, Playlist, PlaylistSchedule, PlayHistory, Announcement


class MusicSerializer(serializers.ModelSerializer):
    """
    Müzik modelini serialize eden sınıf.
    Müzik nesnelerini JSON formatına dönüştürmek için kullanılır.
    """
    class Meta:
        model = Music  # Hangi modelin serialize edileceği
        fields = ['id', 'title', 'artist', 'file', 'created_at']  # Serialize edilecek alanlar


class PlaylistSerializer(serializers.ModelSerializer):
    """
    Çalma listesi modelini serialize eden sınıf.
    Çalma listesi nesnelerini JSON formatına dönüştürmek için kullanılır.
    İçindeki müzikleri de dahil eder.
    """
    musics = MusicSerializer(many=True, read_only=True)  # Çalma listesine ait müzikleri serialize eder

    class Meta:
        model = Playlist  # Hangi modelin serialize edileceği
        fields = ['id', 'name', 'musics', 'created_at']  # Serialize edilecek alanlar


class PlaylistScheduleSerializer(serializers.ModelSerializer):
    """
    Çalma listesi zamanlama modelini serialize eden sınıf.
    Zamanlama nesnelerini JSON formatına dönüştürmek için kullanılır.
    İçindeki çalma listesini de dahil eder.
    """
    playlist = PlaylistSerializer(read_only=True)  # İlişkili çalma listesini serialize eder

    class Meta:
        model = PlaylistSchedule  # Hangi modelin serialize edileceği
        fields = ['id', 'playlist', 'start_time', 'end_time', 'days_of_week']  # Serialize edilecek alanlar


class PlayHistorySerializer(serializers.ModelSerializer):
    """
    Çalma geçmişi modelini serialize eden sınıf.
    Çalma geçmişi nesnelerini JSON formatına dönüştürmek için kullanılır.
    """
    class Meta:
        model = PlayHistory  # Hangi modelin serialize edileceği
        fields = ['music', 'played_at', 'name', 'store_name']  # Serialize edilecek alanlar


class AnnouncementSerializer(serializers.ModelSerializer):
    """
    Anons modelini serialize eden sınıf.
    Anons nesnelerini JSON formatına dönüştürmek için kullanılır.
    """
    class Meta:
        model = Announcement  # Hangi modelin serialize edileceği
        fields = ['audio_file', 'store_name', 'frequency']  # Serialize edilecek alanlar
