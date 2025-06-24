from django.contrib import admin
from .models import Enquete, Opcao, Voto
from django.utils import timezone

@admin.register(Enquete)
class EnqueteAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'get_status', 'data_criacao', 'expires_at', 'delete_at')
    list_filter = ('expires_at',)
    search_fields = ('titulo',)
    ordering = ('-data_criacao',)

    def get_status(self, obj):
        return "Aberta" if obj.expires_at > timezone.now() else "Encerrada"

    get_status.short_description = 'Status'


@admin.register(Opcao)
class OpcaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'enquete', 'texto_opcao', 'votos')
    list_filter = ('enquete',)
    search_fields = ('texto_opcao',)


@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_participante', 'enquete', 'opcao_escolhida', 'data_voto')
    list_filter = ('enquete',)
    search_fields = ('id_participante',)