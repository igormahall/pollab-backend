from rest_framework import serializers
from .models import Enquete, Opcao

class OpcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcao
        fields = ['id', 'texto_opcao', 'votos']

class EnqueteSerializer(serializers.ModelSerializer):
    # Este campo é para LEITURA (quando pedimos os detalhes de uma enquete)
    opcoes = OpcaoSerializer(many=True, read_only=True)

    # Este campo é para ESCRITA (quando criamos uma nova enquete)
    # Ele espera uma lista de strings, ex: ["Opção 1", "Opção 2"]
    opcoes_input = serializers.ListField(
        child=serializers.CharField(max_length=255),
        write_only=True
    )

    class Meta:
        model = Enquete
        # Adicione 'opcoes_input' aos fields para que ele seja aceito no POST
        fields = ['id', 'titulo', 'data_criacao', 'status', 'opcoes', 'opcoes_input']

    def create(self, validated_data):
        """
        Sobrescreve o método create padrão para lidar com a criação
        aninhada das opções.
        """
        # 1. Pega os textos das opções e os remove dos dados validados
        opcoes_data = validated_data.pop('opcoes_input')

        # 2. Cria o objeto Enquete principal
        enquete = Enquete.objects.create(**validated_data)

        # 3. Itera sobre os textos das opções e cria cada objeto Opcao
        for texto_opcao in opcoes_data:
            Opcao.objects.create(enquete=enquete, texto_opcao=texto_opcao)

        return enquete

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