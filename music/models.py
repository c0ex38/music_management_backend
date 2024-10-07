# music/models.py
from django.db import models
from django.utils import timezone

class Store(models.Model):
    """
    Mağaza modelini temsil eder.
    Her mağaza, bir isim ile tanımlanır.
    """
    name = models.CharField(max_length=100)  # Mağaza adı, en fazla 100 karakter uzunluğunda

    def __str__(self):
        # Mağaza adı olarak döner
        return self.name


class Music(models.Model):
    """
    Müzik dosyasını temsil eder.
    Her müzik, bir başlık, sanatçı ve dosya ile tanımlanır.
    """
    title = models.CharField(max_length=255)  # Müzik başlığı, en fazla 255 karakter
    artist = models.CharField(max_length=255)  # Sanatçı adı, en fazla 255 karakter
    file = models.FileField(upload_to='music/')  # Müzik dosyası, 'music/' dizinine yüklenir
    created_at = models.DateTimeField(auto_now_add=True)  # Müzik kaydedildiği zaman otomatik olarak ayarlanır

    def __str__(self):
        # Müzik başlığı ve sanatçı adı ile döner
        return f"{self.title} by {self.artist}"


class Playlist(models.Model):
    """
    Çalma listesi modelini temsil eder.
    Her çalma listesi, bir isim ve mağaza ile ilişkilendirilir.
    """
    name = models.CharField(max_length=100)  # Çalma listesi adı, en fazla 100 karakter
    store_name = models.CharField(max_length=100)  # Mağaza adı, en fazla 100 karakter
    musics = models.ManyToManyField(Music)  # Çalma listesine ait müzikler
    created_at = models.DateTimeField(auto_now_add=True)  # Çalma listesi oluşturulduğu zaman otomatik olarak ayarlanır

    def __str__(self):
        # Çalma listesi adı ve mağaza adı ile döner
        return f"{self.name} - {self.store_name}"


class Announcement(models.Model):
    """
    Anons modelini temsil eder.
    Her anons, bir mağaza ile ilişkilendirilir ve ses dosyası içerir.
    """
    store_name = models.CharField(max_length=100)  # Mağaza adı, en fazla 100 karakter
    audio_file = models.FileField(upload_to='uploads/announcements/')  # Anons için ses dosyası, 'uploads/announcements/' dizinine yüklenir
    frequency = models.PositiveIntegerField(default=3)  # Anonsun kaç şarkıdan sonra çalacağını belirten pozitif tam sayı

    def __str__(self):
        # Anons bilgisi olarak döner
        return f"Announcement for {self.store_name}"


class PlaylistSchedule(models.Model):
    """
    Çalma listesi zamanlama modelini temsil eder.
    Çalma listesi için başlangıç ve bitiş zamanları ile günleri içerir.
    """
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)  # İlişkili çalma listesi
    start_time = models.TimeField()  # Çalma listesi ne zaman başlayacak
    end_time = models.TimeField()  # Çalma listesi ne zaman bitecek
    days_of_week = models.CharField(max_length=100)  # Hangi günlerde çalınacağını belirtir (örneğin: 'Mon,Tue,Wed')

    def __str__(self):
        # Zamanlama bilgisi olarak döner
        return f"Schedule for {self.playlist.name}"


class PlayHistory(models.Model):
    """
    Çalma geçmişi modelini temsil eder.
    Her kayıt, çalınan müzik, zaman, kullanıcı adı ve mağaza adı ile ilişkilendirilir.
    """
    music = models.ForeignKey('Music', on_delete=models.CASCADE)  # İlişkili müzik
    played_at = models.DateTimeField(default=timezone.now)  # Müziğin çalındığı zaman
    name = models.CharField(max_length=100, blank=True, null=True)  # Kullanıcı adı (isteğe bağlı)
    store_name = models.CharField(max_length=100, blank=True, null=True)  # Mağaza adı (isteğe bağlı)

    def __str__(self):
        # Çalma geçmişi bilgisi olarak döner
        return f"{self.music.title} - {self.played_at} - {self.name} - {self.store_name}"
