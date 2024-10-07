import time
import logging
from django.core.management.base import BaseCommand
from music.models import PlaylistSchedule
from datetime import datetime

# Logger nesnesi oluşturarak loglama işlemleri için kullanacağız
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Scheduled music playback based on time intervals'  # Komut hakkında bilgi

    def handle(self, *args, **kwargs):
        # Sonsuz bir döngü oluşturuyoruz
        while True:
            # Geçerli zamanı al
            current_time = datetime.now().time()
            # Geçerli günü kısa koduyla al (örn: 'Mon', 'Tue')
            current_day = datetime.now().strftime('%a')

            # Zamanlanan çalma listelerini kontrol et
            active_schedules = PlaylistSchedule.objects.filter(
                start_time__lte=current_time,  # Başlangıç zamanından önce veya eşit
                end_time__gte=current_time,    # Bitiş zamanından sonra veya eşit
                days_of_week__icontains=current_day  # Geçerli gün içinde
            )

            # Her bir aktif zamanlama için
            for schedule in active_schedules:
                playlist = schedule.playlist  # Zamanlama ile ilişkilendirilmiş çalma listesini al
                self.stdout.write(self.style.SUCCESS(f"Playing playlist: {playlist.name}"))  # Başarı mesajını yazdır
                logger.info(f"Playing playlist: {playlist.name}")  # Log kaydı oluştur

                # Çalma listesi içindeki her müzik dosyasını çal
                for music in playlist.musics.all():
                    logger.info(f"Playing {music.title} by {music.artist}")  # Müzik çalma logu
                    # Müzik çalma işlemi burada gerçekleştirilebilir (örneğin, ses oynatıcı kullanarak)
                    print(f"Playing {music.title} by {music.artist}")  # Müzik başlığını yazdır

            # 60 saniye bekle, sonra tekrar kontrol et
            time.sleep(60)
