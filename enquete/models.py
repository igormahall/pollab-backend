from django.db import models

class Enquete(models.Model):
    # Definimos as opções para o status aqui
    STATUS_CHOICES = [
        ('Aberta', 'Aberta'),
        ('Fechada', 'Fechada'),
    ]

    titulo = models.CharField(max_length=255)
    data_criacao = models.DateTimeField(auto_now_add=True)
    # Adicionamos a opção 'choices' ao campo de status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Aberta')

    def __str__(self):
        return self.titulo

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
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE)
    opcao_escolhida = models.ForeignKey(Opcao, on_delete=models.CASCADE)
    data_voto = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('id_participante', 'enquete')