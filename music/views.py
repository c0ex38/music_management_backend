# music/views.py

from django.utils.dateparse import parse_date
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Announcement, Music, Playlist, PlaylistSchedule, PlayHistory
from .serializers import AnnouncementSerializer, MusicSerializer, PlaylistSerializer, PlaylistScheduleSerializer, PlayHistorySerializer
from django.db.models import Count
from rest_framework.views import APIView


class PlaylistCreateView(generics.CreateAPIView):
    """
    Çalma listesi oluşturma görünümü.
    Kullanıcı yeni bir çalma listesi oluşturduğunda çağrılır.
    """
    queryset = Playlist.objects.all()  # Tüm çalma listelerini al
    serializer_class = PlaylistSerializer  # Kullanılan serializer sınıfı


class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Çalma listesinin detaylarını görüntüleme, güncelleme ve silme görünümü.
    Belirli bir çalma listesi için işlemleri yönetir.
    """
    queryset = Playlist.objects.all()  # Tüm çalma listelerini al
    serializer_class = PlaylistSerializer  # Kullanılan serializer sınıfı

    def put(self, request, *args, **kwargs):
        # Mevcut çalma listesini günceller
        playlist = self.get_object()  # Çalma listesi nesnesini al
        music_ids = request.data.get('musics', [])  # İstemciden gelen müzik ID'lerini al
        musics = Music.objects.filter(id__in=music_ids)  # İlgili müzikleri al
        playlist.musics.set(musics)  # Çalma listesine müzikleri ekle
        return Response(self.get_serializer(playlist).data)  # Güncellenmiş çalma listesini döndür


class PlaylistListCreateView(generics.ListCreateAPIView):
    """
    Çalma listelerini listeleme ve yeni çalma listeleri oluşturma görünümü.
    """
    queryset = Playlist.objects.all()  # Tüm çalma listelerini al
    serializer_class = PlaylistSerializer  # Kullanılan serializer sınıfı


class PlaylistScheduleListCreateView(generics.ListCreateAPIView):
    """
    Çalma listesi zamanlamalarını listeleme ve yeni zamanlamalar oluşturma görünümü.
    """
    queryset = PlaylistSchedule.objects.all()  # Tüm zamanlamaları al
    serializer_class = PlaylistScheduleSerializer  # Kullanılan serializer sınıfı


class MusicListCreateView(generics.ListCreateAPIView):
    """
    Müzik listesini görüntüleme ve yeni müzik ekleme görünümü.
    """
    queryset = Music.objects.all()  # Tüm müzikleri al
    serializer_class = MusicSerializer  # Kullanılan serializer sınıfı

    def create(self, request, *args, **kwargs):
        # Yeni müzik oluşturma işlemi
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  # Doğrulama
            serializer.save()  # Kaydet
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Başarı durumu döndür
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Hata durumu döndür


class PlayHistoryListCreateView(generics.ListCreateAPIView):
    """
    Çalma geçmişi listesini görüntüleme ve yeni çalma geçmişi kaydı ekleme görünümü.
    """
    queryset = PlayHistory.objects.all()  # Tüm çalma geçmişini al
    serializer_class = PlayHistorySerializer  # Kullanılan serializer sınıfı


class PlayHistoryCreateView(generics.CreateAPIView):
    """
    Yeni bir çalma geçmişi kaydı oluşturma görünümü.
    """
    queryset = PlayHistory.objects.all()  # Tüm çalma geçmişini al
    serializer_class = PlayHistorySerializer  # Kullanılan serializer sınıfı


class MusicUploadView(generics.CreateAPIView):
    """
    Yeni müzik dosyası yükleme görünümü.
    """
    queryset = Music.objects.all()  # Tüm müzikleri al
    serializer_class = MusicSerializer  # Kullanılan serializer sınıfı


class PlayHistoryListView(generics.ListAPIView):
    """
    Çalma geçmişini görüntüleme görünümü.
    Filtreleme işlemleri destekler.
    """
    serializer_class = PlayHistorySerializer  # Kullanılan serializer sınıfı

    def get_queryset(self):
        queryset = PlayHistory.objects.all()  # Tüm çalma geçmişini al
        # Filtreleme için parametreleri al
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        store_name = self.request.query_params.get('store_name')
        music_title = self.request.query_params.get('music_title')
        name = self.request.query_params.get('name')

        # Başlangıç tarihi filtresi
        if start_date:
            queryset = queryset.filter(played_at__gte=parse_date(start_date))
        # Bitiş tarihi filtresi
        if end_date:
            queryset = queryset.filter(played_at__lte=parse_date(end_date))
        # Mağaza adı filtresi
        if store_name:
            queryset = queryset.filter(store_name=store_name)
        # Müzik başlığı filtresi
        if music_title:
            queryset = queryset.filter(music__title__icontains=music_title)
        # Kullanıcı adı filtresi
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset  # Filtrelenmiş sorguyu döndür


class PlayCountStatsView(APIView):
    """
    Mağaza bazında çalma istatistiklerini görüntüleme görünümü.
    Hangi mağazanın ne kadar çaldığını döndürür.

    Örnek Yanıt:
    [
      {"store_name": "Store A", "play_count": 45},
      {"store_name": "Store B", "play_count": 30},
      ...
    ]
    """
    def get(self, request):
        # Mağaza adına göre çalma sayısını al
        data = PlayHistory.objects.values('store_name').annotate(play_count=Count('id')).order_by('-play_count')
        return Response(data)  # İstatistikleri döndür



class PlaylistByStoreView(APIView):
    """
    Mağazaya göre çalma listelerini görüntüleme görünümü.
    Belirli bir mağaza için çalma listesi döndürür.
    """
    def get(self, request):
        store_name = request.query_params.get('store_name')  # Mağaza adını al
        if not store_name:
            return Response({"error": "store_name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)  # Hata döndür

        try:
            playlist = Playlist.objects.get(store_name=store_name)  # Belirtilen mağaza adı ile çalma listesini al
            serializer = PlaylistSerializer(playlist)  # Çalma listesi için serializer uygula
            return Response(serializer.data)  # Çalma listesi verilerini döndür
        except Playlist.DoesNotExist:
            return Response({"error": "No playlist found for this store"}, status=status.HTTP_404_NOT_FOUND)  # Hata döndür


class AnnouncementByStoreView(APIView):
    """
    Mağazaya göre anonsları görüntüleme görünümü.
    Belirli bir mağaza için anonsları döndürür.
    """
    def get(self, request):
        store_name = request.query_params.get('store_name')  # Mağaza adını al
        if not store_name:
            return Response({"error": "store_name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)  # Hata döndür

        try:
            announcements = Announcement.objects.filter(store_name=store_name)  # Belirtilen mağaza adı ile anonsları al
            if not announcements.exists():
                return Response({"error": "No announcements found for this store"}, status=status.HTTP_404_NOT_FOUND)  # Hata döndür

            serializer = AnnouncementSerializer(announcements, many=True)  # Anonslar için serializer uygula
            return Response(serializer.data)  # Anons verilerini döndür
        except Exception as e:
            # Django konsolunda hatayı görmek için
            print("Error in AnnouncementByStoreView:", str(e))
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Hata döndür
