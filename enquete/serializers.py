from rest_framework import serializers
from .models import Enquete, Opcao

class OpcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcao
        fields = ['id', 'texto_opcao', 'votos']

class EnqueteSerializer(serializers.ModelSerializer):
    # Aninha as opções dentro da enquete para facilitar o consumo no frontend
    opcoes = OpcaoSerializer(many=True, read_only=True)

    class Meta:
        model = Enquete
        fields = ['id', 'titulo', 'data_criacao', 'status', 'opcoes']

class VotoInputSerializer(serializers.Serializer):
    """
    Serializer para validar a entrada de um voto. Não está ligado a um modelo.
    """
    id_opcao = serializers.IntegerField()

    # O id_participante virá do frontend, então apenas o definimos aqui.
    # Não vamos criar um campo para ele no formulário da API Navegável,
    # pois a ideia é que ele seja gerado pelo cliente (navegador).
    # Vamos pegá-lo diretamente do request.data na view.
    # Mas para o teste, vamos deixá-lo visível por enquanto.
    id_participante = serializers.CharField(max_length=100)

    class Meta:
        fields = ['id_opcao', 'id_participante']