from django.contrib import admin
from .models import Livro
from django.utils.html import format_html

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_publicacao', 'lido', 'mostrar_capa')
    search_fields = ('titulo', 'autor')
    list_filter = ('lido',)

    def mostrar_capa(self, obj):
        if obj.capa_url:
            return format_html('<img src="{}" width="50" height="75" style="object-fit: cover;" />', obj.capa_url)
        return "Sem capa"

    mostrar_capa.short_description = "Capa"