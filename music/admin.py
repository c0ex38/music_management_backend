from django.contrib import admin
from .models import PlayHistory, Music, Playlist, Announcement

# PlayHistory modelini admin paneline kaydediyoruz
@admin.register(PlayHistory)
class PlayHistoryAdmin(admin.ModelAdmin):
    # Liste görünümünde gösterilecek alanlar
    list_display = ('music', 'name', 'store_name', 'played_at')

    # Arama yapılacak alanlar
    search_fields = ('name', 'store_name', 'music__title')

    # Tarih ve mağaza adıyla filtreleme seçenekleri
    list_filter = ('played_at', 'store_name')

    # Sıralama
    ordering = ('-played_at',)  # En son çalınan müzik en üstte görünsün

    # Sadece görüntüleme amaçlı (tıklanabilir değil)
    readonly_fields = ('played_at',)  # 'played_at' alanı yalnızca okunabilir

# Music modelini admin paneline kaydediyoruz
@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'created_at')  # Görüntüde gösterilecek alanlar
    search_fields = ('title', 'artist')  # Arama yapılacak alanlar
    ordering = ('title',)  # Başlığa göre sıralama

# Playlist modelini admin paneline kaydediyoruz
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Görüntüde gösterilecek alanlar
    search_fields = ('name',)  # Arama yapılacak alanlar
    ordering = ('name',)  # Başlığa göre sıralama

# Announcement modelini admin paneline kaydediyoruz
admin.site.register(Announcement)
