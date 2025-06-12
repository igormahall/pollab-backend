from django.db import models

class Enquete(models.Model):
    titulo = models.CharField(max_length=255)
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Aberta') # 'Aberta', 'Fechada'

    def __str__(self):
        return self.titulo

class Opcao(models.Model):
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE, related_name='opcoes')
    texto_opcao = models.CharField(max_length=255)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.texto_opcao

class Voto(models.Model):
    # O identificador do participante pode vir do frontend (ex: um ID de sessão)
    id_participante = models.CharField(max_length=100)
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE)
    opcao_escolhida = models.ForeignKey(Opcao, on_delete=models.CASCADE)
    data_voto = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que um participante só vote uma vez por enquete
        unique_together = ('id_participante', 'enquete')