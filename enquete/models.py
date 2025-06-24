from django.db import models
from django.utils import timezone

class Enquete(models.Model):
    titulo = models.CharField(max_length=255)
    data_criacao = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(default=timezone.now)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.titulo

    @property
    def status(self):
        """Retorna o status baseado no tempo atual."""
        now = timezone.now()
        if now < self.expires_at:
            return "Aberta"
        elif self.delete_at and now >= self.delete_at:
            return "Para Deletar"
        else:
            return "Encerrada"

class Opcao(models.Model):
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE, related_name='opcoes')
    texto_opcao = models.CharField(max_length=255)
    votos = models.IntegerField(default=0)

    class Meta:
        ordering = ['id']
        # Adicionamos nomes amigáveis para singular e plural
        verbose_name = 'Opção'
        verbose_name_plural = 'Opções'

    def __str__(self):
        return self.texto_opcao

class Voto(models.Model):
    id_participante = models.CharField(max_length=100)
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE, related_name='votos')
    opcao_escolhida = models.ForeignKey(Opcao, on_delete=models.CASCADE, related_name='votos_recebidos')
    data_voto = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('id_participante', 'enquete')